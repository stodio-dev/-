#!/usr/bin/env python3
"""Round-trip, rejection and size tests for CL."""
import re
from pathlib import Path

import cl

# (natural-language English, CL message)
PAIRS = [
    ("Monitoring observed that server srv1 failed. Based on that, it is inferred with 95% confidence "
     "that the cause was memory exhaustion. Both claims are from monitor 'mon' at unix time 1730415600.",
     """#src=mon t=1730415600
@1 obs sys:srv1 has fail
@2 inf res:mem has full conf=.95
@3 inf @2 cause @1 conf=.95"""),
    ("Agent 'ops' orders system srv1 to halt (not kill) it, issued at 1730415700.",
     "cmd sys:srv1 do halt src=ops t=1730415700"),
    ("Agent 'planner' estimates, with 70% confidence, that all data in store 'db2' will be valid "
     "after the update, as of 1730415800.",
     "est all.data:db2 has valid conf=.7 src=planner t=1730415800"),
    ("Agent 'a1' states that it does not know whether link 'l7' is safe, at 1730415900.",
     "unk link:l7 has safe src=a1 t=1730415900"),
    ("Sensor 's3' measured that the value of resource cpu was 92 percent at 1730416000, "
     "and the system is therefore busy, inferred with 99% confidence.",
     """#src=s3 t=1730416000
@1 obs res:cpu has val:92 unit=pct
@2 inf @1 cause busy conf=.99"""),
    ("Request from agent 'q': is it true that process 'etl' is blocked by a rule? Sent at 1730416100.",
     "req proc:etl has !ok src=q t=1730416100"),
]

# messages that MUST be rejected, with expected error code
INVALID = [
    ("inf sys:srv1 cause src=m t=1 conf=.9", "E_SYNTAX"),       # missing object
    ("inf sys:srv1 cause res:mem src=m t=1 conf=.9 x=1", "E_FIELD"),
    ("inf sys:srv1 cause flob:mem src=m t=1 conf=.9", "E_CONCEPT"),
    ("inf sys:srv1 cause res:mem src=m t=1", "E_MISSING"),      # inference without conf
    ("obs sys:srv1 has fail t=1", "E_MISSING"),                 # no source
    ("obs sys:srv1 has fail src=m", "E_MISSING"),               # no time
    ("est sys:srv1 has fail src=m t=1 conf=1.5", "E_VALUE"),
    ("obs sys:srv1 maybe fail src=m t=1", "E_REL"),
    ("guess sys:srv1 has fail src=m t=1", "E_MODE"),
    ("obs @9 has fail src=m t=1", "E_REF"),
    ("obs most.sys:srv1 has fail src=m t=1", "E_QUANT"),
]


def roundtrips(text):
    """True iff parse(dumps(parse(text))) == parse(text); a CLError counts as failure."""
    try:
        stmts, _ = cl.parse(text)
        return cl.parse(cl.dumps(stmts))[0] == stmts
    except cl.CLError:
        return False


def rejects(text, code):
    try:
        cl.parse(text)
        return False
    except cl.CLError as e:
        return e.code == code


def regressions():
    """Tests for fixed bugs R1-R3 (see CHAT_HISTORY.md). Each failed before its fix."""
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"{'ok  ' if cond else 'FAIL'} {name}")
        ok &= bool(cond)

    # R1: precision of conf/dur must survive dumps -> parse
    check("R1 conf with 4 digits round-trips", roundtrips("est sys:a has fail src=m t=1 conf=.9555"))
    check("R1 conf=1 and conf=0 round-trip",
          roundtrips("est sys:a has fail src=m t=1 conf=1") and roundtrips("est sys:a has fail src=m t=1 conf=0"))
    check("R1 dur with fraction round-trips", roundtrips("obs sys:a has fail src=m t=1 dur=0.0004"))
    check("R1 non-finite conf rejected", rejects("est sys:a has fail src=m t=1 conf=nan", "E_VALUE"))
    check("R1 non-finite dur rejected",
          rejects("obs sys:a has fail src=m t=1 dur=inf", "E_VALUE")
          and rejects("obs sys:a has fail src=m t=1 dur=nan", "E_VALUE"))

    # R2: terms that need quoting must survive dumps -> parse
    check("R2 instance with space round-trips", roundtrips('obs "sys:my srv" has fail src=m t=1'))
    check("R2 instance with quote round-trips", roundtrips("""obs "sys:it's" has fail src=m t=1"""))
    check("R2 negated quantified instance with space round-trips",
          roundtrips('obs !all."data:big file" has fail src=m t=1'))
    check("R2 plain terms stay unquoted (no token bloat)",
          "'" not in cl.dumps(cl.parse("obs !sys:srv1 has fail src=m t=1")[0]))

    # R3: lexicon default for scope is applied, omitted on output, overridable
    s, _ = cl.parse("obs sys:a has fail src=m t=1")
    check("R3 scope defaults to all", s[0]["f"].get("scope") == "all")
    check("R3 default scope is omitted by dumps", "scope" not in cl.dumps(s))
    text = "#scope=some src=m t=1\nobs sys:a has fail\nobs sys:b has fail scope=all"
    s, _ = cl.parse(text)
    check("R3 header scope overridden by explicit scope=all",
          s[0]["f"]["scope"] == "some" and s[1]["f"]["scope"] == "all" and roundtrips(text))
    check("R3 default scope not shown in gloss", "scope" not in cl.gloss(cl.parse("obs sys:a has fail src=m t=1")[0]))
    return ok


def v02():
    """Tests for CL v0.2 (R7-R11, relative time, ctx, grouping, compact lexicon).
    Written before the v0.2 implementation; they must fail on v0.1."""
    ok = True

    def check(name, fn):
        nonlocal ok
        try:
            res = bool(fn())
            err = ""
        except Exception as e:                       # a crash counts as failure, with the reason
            res, err = False, f"  ({type(e).__name__}: {e})"
        print(f"{'ok  ' if res else 'FAIL'} {name}{err if not res else ''}")
        ok &= res

    lex = cl.LEX
    codes = set(cl.CONCEPTS) | set(lex["relations"]) | set(lex["modes"])
    items = [(c, k, v) for c in ["entities", "states", "actions", "quantifiers", "relations"]
             for k, v in lex[c].items()]

    def dangling():
        bad = []
        for c, k, v in items:
            for part in re.split(r"[;,]", v.get("not", "")):
                head = part.strip().split(" ")[0].split("(")[0]
                if head and head not in codes:
                    bad.append(f"{k}->{head}")
        return bad

    # R7: definitions and contrasts are complete and resolvable
    check("R7 every concept and relation has def and not",
          lambda: all(v.get("def") and v.get("not") for _, _, v in items))
    check("R7 every 'not' contrast names an existing code", lambda: not dangling() or print("     dangling:", dangling()))

    # R8: modifiers removed (no defined grammatical role)
    check("R8 modifiers category removed", lambda: "modifiers" not in lex)
    check("R8 'more' is no longer a concept", lambda: rejects("obs sys:a has more src=m t=1", "E_CONCEPT"))

    # R9: negated relation
    check("R9 '!cause' parses with rneg=True",
          lambda: cl.parse("inf sys:a !cause sys:b conf=.9 src=m t=1")[0][0]["rneg"] is True)
    check("R9 plain relation has rneg=False", lambda: cl.parse("obs sys:a has fail src=m t=1")[0][0]["rneg"] is False)
    check("R9 negated relation round-trips", lambda: roundtrips("inf sys:a !cause sys:b conf=.9 src=m t=1"))
    check("R9 gloss shows NOT CAUSE",
          lambda: "NOT CAUSE" in cl.gloss(cl.parse("inf sys:a !cause sys:b conf=.9 src=m t=1")[0]))
    check("R9 'obs ... !cause' still warns", lambda: bool(cl.parse("obs sys:a !cause sys:b src=m t=1")[1]))

    # R10: forecasts get their own mode; dur has one definition
    check("R10 pred mode parses", lambda: cl.parse("pred sys:db has full conf=.6 dur=3600 src=m t=1")[0])
    check("R10 pred requires dur", lambda: rejects("pred sys:db has full conf=.6 src=m t=1", "E_MISSING"))
    check("R10 pred requires conf", lambda: rejects("pred sys:db has full dur=60 src=m t=1", "E_MISSING"))
    check("R10 pred has a gloss label", lambda: "pred" in cl.MODE_LABEL)
    check("R10 dur definition names the interval [t, t+dur]", lambda: "t+dur" in lex["fields"]["dur"]["def"])

    # R11: ack must point at the acknowledged statement
    check("R11 ack with a non-reference subject is rejected", lambda: rejects("ack sys:a has recv src=m t=1", "E_SYNTAX"))
    check("R11 canonical 'ack @N has recv' parses",
          lambda: cl.parse("@1 cmd proc:x do halt src=o t=1\nack @1 has recv src=w t=2")[0])

    # relative time
    absol = "obs sys:a has fail src=m t=1730500197"
    check("time: t=+N resolves against #t0", lambda: cl.parse("#t0=1730500000\nobs sys:a has fail src=m t=+197")[0]
          == cl.parse(absol)[0])
    check("time: t0 and relative t in one header, either order",
          lambda: cl.parse("#t=+197 t0=1730500000 src=m\nobs sys:a has fail")[0] == cl.parse(absol)[0])
    check("time: t=+N without t0 is rejected", lambda: rejects("obs sys:a has fail src=m t=+5", "E_MISSING"))
    check("time: t0 inside a statement is rejected", lambda: rejects("obs sys:a has fail src=m t=1 t0=0", "E_FIELD"))
    check("time: t0 is not stored in statement fields",
          lambda: "t0" not in cl.parse("#t0=10\nobs sys:a has fail src=m t=+1")[0][0]["f"])
    two = "obs sys:a has fail src=m t=1730500197\nobs sys:b has ok src=n t=1730500299"
    check("time: dumps writes relative times when t differs",
          lambda: "#t0=" in cl.dumps(cl.parse(two)[0]) and "t=+" in cl.dumps(cl.parse(two)[0]) and roundtrips(two))

    # ctx: which incident/document a statement belongs to (models invented scope=d01 for this)
    check("ctx: field parses", lambda: cl.parse("obs sys:a has fail src=m t=1 ctx=d01")[0][0]["f"]["ctx"] == "d01")
    check("ctx: header applies to following lines",
          lambda: cl.parse("#ctx=d02 src=m t=1\nobs sys:a has fail")[0][0]["f"]["ctx"] == "d02")
    check("ctx: whitespace in ctx is rejected", lambda: rejects('obs sys:a has fail src=m t=1 "ctx=a b"', "E_VALUE"))

    # grouping: runs of equal values become header changes; nothing leaks to statements without the field
    runs = "\n".join([f"obs sys:a{i} has fail src=aa t={i}" for i in range(3)]
                     + [f"obs sys:b{i} has ok src=bb t={10 + i}" for i in range(3)])
    out = lambda: cl.dumps(cl.parse(runs)[0])
    check("group: source runs become headers",
          lambda: "#src=aa" in out() and "#src=bb" in out() and roundtrips(runs))
    check("group: no inline src left on statement lines",
          lambda: not any("src=" in l for l in out().splitlines() if not l.startswith("#")))
    mixed = "inf sys:a cause sys:b conf=.9 src=m t=1\nobs sys:c has ok src=m t=2\ninf sys:d cause sys:e conf=.9 src=m t=3"
    check("group: a field missing from some statements never leaks via a header", lambda: roundtrips(mixed))

    # the example in SPEC.md must stay valid
    def spec_example():
        spec = (Path(__file__).parent / "SPEC.md").read_text()
        block = spec.split("## Example", 1)[1].split("```", 2)[1]
        return cl.parse(block)[0] and not cl.parse(block)[1]
    check("SPEC.md example parses with no warnings", spec_example)

    # compact lexicon for transport stays in sync with lexicon.json
    lt = Path(__file__).parent / "lexicon.txt"
    check("lexicon.txt exists and equals cl.lexicon_text()", lambda: lt.read_text() == cl.lexicon_text())
    return ok


def scenarios():
    """Every experiment scenario written in CL must parse with no error and no warning."""
    ok = True
    root = Path(__file__).parent
    files = sorted((root / "experiment").rglob("scenarios/*.cl"))
    if len(files) < 12:                     # 8 in v1 + 4 in v2
        print(f"FAIL expected at least 12 experiment scenarios, found {len(files)}")
        return False
    for p in files:
        try:
            stmts, warns = cl.parse(p.read_text())
            good = bool(stmts) and not warns and cl.parse(cl.dumps(stmts))[0] == stmts
        except cl.CLError as e:
            print(f"FAIL {p.relative_to(root)}: {e}")
            good = False
        if good:
            print(f"ok   {p.relative_to(root)} parses and round-trips")
        ok &= good
    return ok


def main():
    ok = True
    tot_nl = tot_cl = 0
    method = ""
    print(f"{'#':>2} {'NL tok':>7} {'CL tok':>7} {'saving':>7}  roundtrip")
    for i, (nl, text) in enumerate(PAIRS, 1):
        stmts, warns = cl.parse(text)
        again, _ = cl.parse(cl.dumps(stmts))
        rt = again == stmts
        ok &= rt
        n_nl, method = cl.count_tokens(nl)
        n_cl, _ = cl.count_tokens(cl.dumps(stmts))
        tot_nl, tot_cl = tot_nl + n_nl, tot_cl + n_cl
        print(f"{i:>2} {n_nl:>7} {n_cl:>7} {100 * (1 - n_cl / n_nl):>6.0f}%  {'ok' if rt else 'FAIL'}")
    print(f"   {tot_nl:>7} {tot_cl:>7} {100 * (1 - tot_cl / tot_nl):>6.0f}%   (counter: {method})\n")

    for text, code in INVALID:
        try:
            cl.parse(text)
            print(f"FAIL accepted: {text}")
            ok = False
        except cl.CLError as e:
            hit = e.code == code
            ok &= hit
            print(f"{'ok  ' if hit else 'FAIL'} {e.code:10} <- {text}")

    _, warns = cl.parse("obs sys:srv1 cause res:mem src=m t=1")
    print("\nwarning test:", "ok" if warns else "FAIL")
    ok &= bool(warns)

    print("\nregressions (R1-R3):")
    ok &= regressions()

    print("\nv0.2:")
    ok &= v02()

    print("\nexperiment scenarios:")
    ok &= scenarios()
    print("\nALL PASS" if ok else "\nFAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
