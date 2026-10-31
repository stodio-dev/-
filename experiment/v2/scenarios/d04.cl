@1 obs sys:juliet has busy src=sre t=1730530378
@2 obs sys:india has fail src=auditor t=1730532478
@3 obs sys:alpha has fail src=opsbot t=1730530455
obs sys:foxtrot has ok src=opsbot t=1730532170
@4 obs sys:echo has busy src=mon t=1730531869
obs sys:bravo has fail src=auditor t=1730531050
obs sys:delta has fail src=sre t=1730530651
obs sys:hotel has idle src=mon t=1730532667
@5 cmd proc:reindex do halt src=ops t=1730532814
inf @4 cause @3 conf=.8 src=mon t=1730532590
est sys:echo has full conf=.95 dur=86400 src=auditor t=1730531484
inf @2 cause event:sla_breach conf=.55 src=auditor t=1730532408
cmd proc:cleanup do kill src=ops t=1730532352
unk sys:golf has ok src=sre t=1730531463
est sys:juliet has full conf=.85 dur=7200 src=auditor t=1730530812
ack @5 to agent:worker src=worker t=1730532051
inf @1 cause @2 conf=.9 src=mon t=1730532079
unk sys:charlie has ok src=auditor t=1730532625
