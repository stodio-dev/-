model: grok-4.5
condition: relay-cl
run: 2
hop: 2
---
#scope=d1 src=sre
@12 obs sys:web2 has fail t=1730502751
@13 obs sys:cache1 has fail t=1730500728
obs sys:queue1 has fail t=1730500637
obs sys:web3 has fail t=1730500672
est sys:db1 has full conf=.8 dur=1800 t=1730501442
unk sys:db2 has ok t=1730501239
#src=mon
obs sys:db3 has idle t=1730501197
@14 obs sys:cache2 has busy t=1730500504
est sys:cache2 has full conf=.55 dur=7200 t=1730500749
#src=auditor
@11 obs sys:db1 has busy t=1730501106
unk sys:web1 has ok t=1730501323
inf @12 cause event:sla_breach conf=.95 t=1730502989
#src=ops
@15 cmd proc:backup do halt t=1730501652
cmd proc:etl do kill t=1730501988
#src=opsbot
obs sys:queue2 has ok t=1730500819
inf @14 cause @13 conf=.85 t=1730501463
#src=worker
ack @15 to agent:worker t=1730500987
#src=sre
inf @11 cause @12 conf=.9 t=1730502240
#scope=d2 src=mon
@21 obs sys:gw-ap has fail t=1730510315
@22 obs sys:auth2 has busy t=1730512758
@23 obs sys:search2 has fail t=1730511309
est sys:gw-eu has full conf=.95 dur=1800 t=1730510742
est sys:ml1 has full conf=.65 dur=7200 t=1730511512
#src=opsbot
obs sys:auth1 has fail t=1730511687
@24 obs sys:ml1 has busy t=1730512814
inf @21 cause event:sla_breach conf=.6 t=1730511442
unk sys:pay2 has ok t=1730511162
#src=sre
obs sys:gw-us has ok t=1730511589
obs sys:gw-eu has ok t=1730511925
obs sys:pay1 has stop t=1730510686
inf @22 cause @21 conf=.55 t=1730512282
#src=ops
cmd proc:report do kill t=1730511540
@25 cmd proc:etl do halt t=1730510224
#src=auditor
unk sys:search1 has ok t=1730510854
inf @24 cause @23 conf=.85 t=1730512835
#src=worker
ack @25 to agent:worker t=1730511673
#scope=d3 src=opsbot
obs sys:node11 has stop t=1730521582
@32 obs sys:node15 has fail t=1730521827
@33 obs sys:node23 has busy t=1730522898
obs sys:node09 has fail t=1730522471
#src=auditor
obs sys:node12 has ok t=1730520301
@34 obs sys:node14 has busy t=1730520189
unk sys:node21 has ok t=1730522177
unk sys:node07 has ok t=1730520658
inf @34 cause @32 conf=.9 t=1730521792
#src=mon
@31 obs sys:node08 has fail t=1730520812
est sys:node12 has full conf=.85 dur=7200 t=1730522555
#src=ops
cmd proc:etl do kill t=1730521883
@35 cmd proc:reindex do halt t=1730521897
#src=opsbot
inf @31 cause event:sla_breach conf=.8 t=1730522996
inf @33 cause @31 conf=.95 t=1730522058
#src=sre
obs sys:node22 has fail t=1730520455
est sys:node14 has full conf=.65 dur=3600 t=1730520791
#src=worker
ack @35 to agent:worker t=1730520518
#scope=d4 src=auditor
@42 obs sys:india has fail t=1730532478
obs sys:bravo has fail t=1730531050
est sys:echo has full conf=.95 dur=86400 t=1730531484
est sys:juliet has full conf=.85 dur=7200 t=1730530812
unk sys:charlie has ok t=1730532625
inf @42 cause event:sla_breach conf=.55 t=1730532408
#src=sre
@41 obs sys:juliet has busy t=1730530378
obs sys:delta has fail t=1730530651
unk sys:golf has ok t=1730531463
#src=mon
@44 obs sys:echo has busy t=1730531869
obs sys:hotel has idle t=1730532667
inf @41 cause @42 conf=.9 t=1730532079
#src=ops
@45 cmd proc:reindex do halt t=1730532814
cmd proc:cleanup do kill t=1730532352
#src=opsbot
@43 obs sys:alpha has fail t=1730530455
obs sys:foxtrot has ok t=1730532170
#src=mon
inf @44 cause @43 conf=.8 t=1730532590
#src=worker
ack @45 to agent:worker t=1730532051
