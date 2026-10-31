obs sys:db3 has idle src=mon t=1730501197
obs sys:queue2 has ok src=opsbot t=1730500819
@1 obs sys:db1 has busy src=auditor t=1730501106
@2 obs sys:web2 has fail src=sre t=1730502751
@3 obs sys:cache1 has fail src=sre t=1730500728
obs sys:queue1 has fail src=sre t=1730500637
@4 obs sys:cache2 has busy src=mon t=1730500504
obs sys:web3 has fail src=sre t=1730500672
est sys:cache2 has full conf=.55 dur=7200 src=mon t=1730500749
@5 cmd proc:backup do halt src=ops t=1730501652
inf @4 cause @3 conf=.85 src=opsbot t=1730501463
inf @1 cause @2 conf=.9 src=sre t=1730502240
cmd proc:etl do kill src=ops t=1730501988
ack @5 to agent:worker src=worker t=1730500987
est sys:db1 has full conf=.8 dur=1800 src=sre t=1730501442
unk sys:db2 has ok src=sre t=1730501239
unk sys:web1 has ok src=auditor t=1730501323
inf @2 cause event:sla_breach conf=.95 src=auditor t=1730502989
