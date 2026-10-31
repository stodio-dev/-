#!/usr/bin/env python3
"""Round-trip, rejection and size tests for CL."""
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
    print("\nALL PASS" if ok else "\nFAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
