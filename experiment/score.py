#!/usr/bin/env python3
"""Score experiment results against a PRIVATE answer key (never commit the key).

usage: python3 experiment/score.py KEY.json [RESULTS_DIR] [--out REPORT.md]

RESULTS_DIR is experiment/results (v1) or experiment/v2/results (v2).
Result file (<model>__<track>__run<N>.md) has header lines `model:`, `track:`, `run:` and one
answer per line, e.g. `s01.q1: B`. Tracks: nl, cl, relay-nl, relay-cl.
Missing, malformed or contradicting answers count as wrong.
For v2, hop messages in ../relay/ are checked against ../relay-budget.txt.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cl  # noqa: E402

TRACKS = ("nl", "cl", "relay-nl", "relay-cl")
ANSWER = re.compile(r"^\s*[-*]?\s*\**([a-z]\d\d\.q\d+)\**\s*[:=]\s*\**\s*([A-Ea-e])\b")
META = re.compile(r"^\s*(model|track|run|condition|hop)\s*:\s*(.+?)\s*$", re.I)


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


def read_hop(path):
    """Return (meta, body_chars). The body is everything after the first '---' line."""
    lines = path.read_text(errors="replace").splitlines()
    meta, body_start = {}, None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            body_start = i + 1
            break
        m = META.match(line)
        if m:
            meta.setdefault(m.group(1).lower(), m.group(2).strip().lower())
    if body_start is None:
        body = "\n".join(line for line in lines if not META.match(line))
    else:
        body = "\n".join(lines[body_start:])
    parts = path.stem.split("__")
    if len(parts) == 4:
        meta.setdefault("model", parts[0].lower())
        meta.setdefault("condition", parts[1].lower())
        meta.setdefault("run", re.sub(r"\D", "", parts[2]) or "?")
        meta.setdefault("hop", re.sub(r"\D", "", parts[3]) or "?")
    return meta, len(body.strip())


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
    base = rdir.resolve().parent                       # experiment/ or experiment/v2/
    files = sorted(p for p in rdir.glob("*.md") if p.name.lower() != "readme.md")

    runs = []
    for p in files:
        meta, ans, conflicts = read_result(p)
        issues = []
        if "model" not in meta or meta.get("track") not in TRACKS:
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
            L.append(f"| {model} | {track} | {len(rs)} | {pct(mean[(model, track)])} | "
                     f"{pct(min(accs))} | {pct(max(accs))} |")

        comparisons = (("CL - NL (direct)", "nl", "cl"), ("CL - NL (relay)", "relay-nl", "relay-cl"),
                       ("NL: relay - direct", "nl", "relay-nl"), ("CL: relay - direct", "cl", "relay-cl"))
        rows = []
        for model in sorted({m for m, _ in grp}):
            for name, a, b in comparisons:
                if (model, a) in mean and (model, b) in mean:
                    rows.append(f"| {model} | {name} | {pct(mean[(model, a)])} | {pct(mean[(model, b)])} | "
                                f"{100 * (mean[(model, b)] - mean[(model, a)]):+.1f} |")
        if rows:
            L += ["", "## Comparisons (percentage points, same model)", "",
                  "| model | comparison | first | second | second - first |", "|---|---|---:|---:|---:|"] + rows

        tracks = [t for t in TRACKS if any(r["track"] == t for r in runs)]
        cats = sorted({c["category"] for c in key.values()})
        L += ["", "## Accuracy by category (all models and runs pooled)", "",
              "| category | questions | " + " | ".join(tracks) + " |",
              "|---|---:|" + "---:|" * len(tracks)]
        for c in cats:
            n = sum(1 for v in key.values() if v["category"] == c)
            cells = []
            for t in tracks:
                rs = [r for r in runs if r["track"] == t]
                tot = sum(r["by_cat"][c][1] for r in rs)
                cells.append(pct(sum(r["by_cat"][c][0] for r in rs) / tot) if tot else "-")
            L.append(f"| {c} | {n} | " + " | ".join(cells) + " |")

    problems = [f"- {r['file']}: {', '.join(r['issues'])}" for r in runs if r["issues"]]

    relay_dir = base / "relay"
    if relay_dir.exists():
        hops = sorted(p for p in relay_dir.glob("*.md") if p.name.lower() != "readme.md")
        budget = None
        bf = base / "relay-budget.txt"
        if bf.exists():
            budget = int(bf.read_text().strip())
        if hops:
            L += ["", f"## Relay hop messages (budget: {budget if budget else 'unknown'} characters)", "",
                  "| model | condition | run | hop | characters | within budget |", "|---|---|---|---|---:|---|"]
            for p in hops:
                meta, n = read_hop(p)
                within = "-" if budget is None else ("yes" if n <= budget else "NO")
                L.append(f"| {meta.get('model', '?')} | {meta.get('condition', '?')} | {meta.get('run', '?')} | "
                         f"{meta.get('hop', '?')} | {n} | {within} |")
                if budget is not None and n > budget:
                    problems.append(f"- {p.name}: {n} characters, over the {budget} budget "
                                    f"(treat this chain's result with care)")

    if problems:
        L += ["", "## Files with problems", ""] + problems

    sizes = {}
    for name, paths in (("NL track", [base / "track-nl.md"]), ("CL track", [base / "track-cl.md"]),
                        ("CL track + SPEC.md + lexicon.json",
                         [base / "track-cl.md", HERE.parent / "SPEC.md", HERE.parent / "lexicon.json"])):
        try:
            text = "\n".join(p.read_text() for p in paths)
            sizes[name] = cl.count_tokens(text)
        except OSError:
            pass
    if sizes:
        method = next(iter(sizes.values()))[1]
        L += ["", f"## Input size ({method})", "", "| input | tokens |", "|---|---:|"]
        L += [f"| {k} | {v[0]} |" for k, v in sizes.items()]
        L += ["", "The CL track pays once for SPEC.md and lexicon.json; the NL track does not. "
              "Use the API's real token counts for a decision."]

    text = "\n".join(L) + "\n"
    if out:
        Path(out).write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
