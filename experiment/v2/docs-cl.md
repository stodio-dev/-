# Documents (CL)

Four incident logs written in CL (Concept Language, defined by SPEC.md and lexicon.json). Questions are provided separately.

---

## d01

```cl
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
```

---

## d02

```cl
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
```

---

## d03

```cl
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
```

---

## d04

```cl
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
```

