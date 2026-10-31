obs sys:node11 has stop src=opsbot t=1730521582
@1 obs sys:node08 has fail src=mon t=1730520812
@2 obs sys:node15 has fail src=opsbot t=1730521827
obs sys:node22 has fail src=sre t=1730520455
obs sys:node12 has ok src=auditor t=1730520301
@3 obs sys:node23 has busy src=opsbot t=1730522898
@4 obs sys:node14 has busy src=auditor t=1730520189
obs sys:node09 has fail src=opsbot t=1730522471
est sys:node14 has full conf=.65 dur=3600 src=sre t=1730520791
est sys:node12 has full conf=.85 dur=7200 src=mon t=1730522555
unk sys:node21 has ok src=auditor t=1730522177
cmd proc:etl do kill src=ops t=1730521883
inf @4 cause @2 conf=.9 src=auditor t=1730521792
@5 cmd proc:reindex do halt src=ops t=1730521897
unk sys:node07 has ok src=auditor t=1730520658
inf @1 cause event:sla_breach conf=.8 src=opsbot t=1730522996
inf @3 cause @1 conf=.95 src=opsbot t=1730522058
ack @5 to agent:worker src=worker t=1730520518
