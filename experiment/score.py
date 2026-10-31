#!/usr/bin/env python3
"""Score experiment results against a PRIVATE answer key (never commit the key).

usage: python3 experiment/score.py KEY.json [RESULTS_DIR] [--out REPORT.md]

Result file (experiment/results/<model>__<track>__run<N>.md) contains header lines
`model:`, `track:`, `run:` and one answer per line, e.g. `s01.q1: B`.
Missing, malformed or contradicting answers count as wrong.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cl  # noqa: E402

ANSWER = re.compile(r"^\s*[-*]?\s*\**(s\d\d\.q\d)\**\s*[:=]\s*\**\s*([A-Ea-e])\b")
META = re.compile(r"^\s*(model|track|run)\s*:\s*(.+?)\s*$", re.I)


def read_result(path):
    meta, ans, conflicts = {}, {}, set()
    for line in path.read_text(errors="replace").splitlines():
        m = META.match(line)
        if m:
            meta.setdefault(m.group(1).lower(), m.group(2).strip().lower())
            continue
        m = ANSWER.match(line)
        if m:
            q, a = m.group(1), m.group(2).upper()
            if q in ans and ans[q] != a:
                conflicts.add(q)
            ans.setdefault(q, a)
    parts = path.stem.split("__")
    if len(parts) == 3:
        meta.setdefault("model", parts[0].lower())
        meta.setdefault("track", parts[1].lower())
        meta.setdefault("run", re.sub(r"\D", "", parts[2]) or "?")
    return meta, ans, conflicts


def pct(x):
    return f"{100 * x:.1f}%"


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    out = argv[argv.index("--out") + 1] if "--out" in argv else None
    if out:
        args = [a for a in args if a != out]
    if not args:
        print(__doc__)
        return 2
    key = json.loads(Path(args[0]).read_text())
    key.pop("_meta", None)
    rdir = Path(args[1]) if len(args) > 1 else HERE / "results"
    files = sorted(p for p in rdir.glob("*.md") if p.name.lower() != "readme.md")

    runs = []          # dicts: model, track, run, correct, total, by_cat, issues
    for p in files:
        meta, ans, conflicts = read_result(p)
        issues = []
        if not all(k in meta for k in ("model", "track")) or meta.get("track") not in ("nl", "cl"):
            issues.append("missing/invalid model or track header")
        missing = [q for q in key if q not in ans]
        if missing:
            issues.append(f"{len(missing)} missing answers")
        if conflicts:
            issues.append(f"{len(conflicts)} contradicting duplicates")
        extra = [q for q in ans if q not in key]
        if extra:
            issues.append(f"{len(extra)} unknown question ids")
        by_cat = defaultdict(lambda: [0, 0])
        correct = 0
        for q, spec in key.items():
            ok = ans.get(q) == spec["answer"] and q not in conflicts
            correct += ok
            by_cat[spec["category"]][0] += ok
            by_cat[spec["category"]][1] += 1
        runs.append(dict(file=p.name, model=meta.get("model", "?"), track=meta.get("track", "?"),
                         run=meta.get("run", "?"), correct=correct, total=len(key),
                         by_cat=by_cat, issues=issues))

    L = ["# Experiment report", "", f"Questions: {len(key)} | result files: {len(runs)}", ""]
    if not runs:
        L.append("No result files found.")
    else:
        grp = defaultdict(list)
        for r in runs:
            grp[(r["model"], r["track"])].append(r)

        L += ["## Accuracy by model and track", "",
              "| model | track | runs | mean | min | max |", "|---|---|---:|---:|---:|---:|"]
        mean = {}
        for (model, track), rs in sorted(grp.items()):
            accs = [r["correct"] / r["total"] for r in rs]
            mean[(model, track)] = sum(accs) / len(accs)
            L.append(f"| {model} | {track} | {len(rs)} | {pct(mean[(model, track)])} | {pct(min(accs))} | {pct(max(accs))} |")

        models = sorted({m for m, _ in grp})
        both = [m for m in models if (m, "nl") in mean and (m, "cl") in mean]
        if both:
            L += ["", "## CL minus NL (percentage points, same model)", "",
                  "| model | NL | CL | CL - NL |", "|---|---:|---:|---:|"]
            for m in both:
                L.append(f"| {m} | {pct(mean[(m, 'nl')])} | {pct(mean[(m, 'cl')])} | "
                         f"{100 * (mean[(m, 'cl')] - mean[(m, 'nl')]):+.1f} |")

        cats = sorted({c["category"] for c in key.values()})
        L += ["", "## Accuracy by category (all models and runs pooled)", "",
              "| category | questions | NL | CL |", "|---|---:|---:|---:|"]
        for c in cats:
            n = sum(1 for v in key.values() if v["category"] == c)
            cell = {}
            for t in ("nl", "cl"):
                rs = [r for r in runs if r["track"] == t]
                tot = sum(r["by_cat"][c][1] for r in rs)
                cell[t] = pct(sum(r["by_cat"][c][0] for r in rs) / tot) if tot else "-"
            L.append(f"| {c} | {n} | {cell['nl']} | {cell['cl']} |")

        bad = [r for r in runs if r["issues"]]
        if bad:
            L += ["", "## Files with problems", ""]
            L += [f"- {r['file']}: {', '.join(r['issues'])}" for r in bad]

    sizes = {}
    for name, files_ in (("NL track", ["track-nl.md"]), ("CL track", ["track-cl.md"]),
                         ("CL track + SPEC.md + lexicon.json", ["track-cl.md", "../SPEC.md", "../lexicon.json"])):
        try:
            text = "\n".join((HERE / f).read_text() for f in files_)
            sizes[name] = cl.count_tokens(text)
        except OSError:
            pass
    if sizes:
        method = next(iter(sizes.values()))[1]
        L += ["", f"## Input size ({method})", "", "| input | tokens |", "|---|---:|"]
        L += [f"| {k} | {v[0]} |" for k, v in sizes.items()]
        L.append("")
        L.append("The CL track pays once for SPEC.md and lexicon.json; the NL track does not. "
                 "Use the API's real token counts for a decision.")

    text = "\n".join(L) + "\n"
    if out:
        Path(out).write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
