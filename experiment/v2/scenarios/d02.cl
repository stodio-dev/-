@1 obs sys:gw-ap has fail src=mon t=1730510315
obs sys:gw-us has ok src=sre t=1730511589
@2 obs sys:auth2 has busy src=mon t=1730512758
obs sys:gw-eu has ok src=sre t=1730511925
@3 obs sys:search2 has fail src=mon t=1730511309
obs sys:pay1 has stop src=sre t=1730510686
obs sys:auth1 has fail src=opsbot t=1730511687
@4 obs sys:ml1 has busy src=opsbot t=1730512814
unk sys:search1 has ok src=auditor t=1730510854
cmd proc:report do kill src=ops t=1730511540
inf @2 cause @1 conf=.55 src=sre t=1730512282
inf @4 cause @3 conf=.85 src=auditor t=1730512835
inf @1 cause event:sla_breach conf=.6 src=opsbot t=1730511442
unk sys:pay2 has ok src=opsbot t=1730511162
est sys:gw-eu has full conf=.95 dur=1800 src=mon t=1730510742
@5 cmd proc:etl do halt src=ops t=1730510224
est sys:ml1 has full conf=.65 dur=7200 src=mon t=1730511512
ack @5 to agent:worker src=worker t=1730511673
