# Dense comprehension experiment (v2), track CL

Four incident logs in CL (defined by SPEC.md and lexicon.json), each followed by its questions.

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

### Questions d01

**d01.q1** Which source reported that cache1 failed?
- A) mon
- B) opsbot
- C) auditor
- D) sre
- E) Cannot be determined from the document

**d01.q2** How is the claim that db1 being busy caused the failure of web2 classified?
- A) Inferred by sre, 90% confidence
- B) Inferred by sre, 85% confidence
- C) Inferred by mon, 90% confidence
- D) Directly observed by sre
- E) Cannot be determined from the document

**d01.q3** What confidence did the forecast for cache2 carry?
- A) 90%
- B) 55%
- C) 85%
- D) 95%
- E) Cannot be determined from the document

**d01.q4** Within what time span is db1 predicted to be full?
- A) 1 hour
- B) 2 hours
- C) 30 minutes
- D) 24 hours
- E) Cannot be determined from the document

**d01.q5** How many servers are reported as failed?
- A) 2
- B) 3
- C) 5
- D) 4
- E) Cannot be determined from the document

**d01.q6** Which of these servers has the latest-dated direct observation of its own state?
- A) cache2
- B) queue1
- C) web2
- D) db3
- E) Cannot be determined from the document

**d01.q7** For which server does the log explicitly say the status could not be determined?
- A) db2
- B) db1
- C) cache1
- D) queue1
- E) Cannot be determined from the document

**d01.q8** Which server was observed to be busy by auditor?
- A) cache2
- B) cache1
- C) db1
- D) queue1
- E) Cannot be determined from the document

**d01.q9** What did ops order for the job etl?
- A) To destroy it irreversibly (kill)
- B) To pause it so that it can be resumed (halt)
- C) To start it (run)
- D) Only to report its status (a request)
- E) Cannot be determined from the document

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

### Questions d02

**d02.q1** Which source reported that gw-ap failed?
- A) opsbot
- B) mon
- C) sre
- D) auditor
- E) Cannot be determined from the document

**d02.q2** How is the claim that auth2 being busy caused the failure of gw-ap classified?
- A) Inferred by sre, 85% confidence
- B) Inferred by mon, 55% confidence
- C) Inferred by sre, 55% confidence
- D) Directly observed by sre
- E) Cannot be determined from the document

**d02.q3** What confidence did the forecast for ml1 carry?
- A) 55%
- B) 85%
- C) 60%
- D) 65%
- E) Cannot be determined from the document

**d02.q4** Within what time span is gw-eu predicted to be full?
- A) 1 hour
- B) 30 minutes
- C) 2 hours
- D) 24 hours
- E) Cannot be determined from the document

**d02.q5** How many servers are reported as failed?
- A) 1
- B) 2
- C) 4
- D) 3
- E) Cannot be determined from the document

**d02.q6** Which of these servers has the latest-dated direct observation of its own state?
- A) pay1
- B) gw-ap
- C) gw-eu
- D) gw-us
- E) Cannot be determined from the document

**d02.q7** For which server does the log explicitly say the status could not be determined?
- A) search2
- B) pay1
- C) pay2
- D) auth2
- E) Cannot be determined from the document

**d02.q8** Which server was observed to be busy by mon?
- A) gw-ap
- B) gw-eu
- C) gw-us
- D) auth2
- E) Cannot be determined from the document

**d02.q9** What did ops order for the job report?
- A) To pause it so that it can be resumed (halt)
- B) To destroy it irreversibly (kill)
- C) To start it (run)
- D) Only to report its status (a request)
- E) Cannot be determined from the document

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

### Questions d03

**d03.q1** Which source reported that node15 failed?
- A) mon
- B) opsbot
- C) sre
- D) auditor
- E) Cannot be determined from the document

**d03.q2** How is the claim that node23 being busy caused the failure of node08 classified?
- A) Inferred by opsbot, 90% confidence
- B) Inferred by mon, 95% confidence
- C) Inferred by opsbot, 95% confidence
- D) Directly observed by opsbot
- E) Cannot be determined from the document

**d03.q3** What confidence did the forecast for node14 carry?
- A) 65%
- B) 95%
- C) 90%
- D) 80%
- E) Cannot be determined from the document

**d03.q4** Within what time span is node12 predicted to be full?
- A) 30 minutes
- B) 2 hours
- C) 1 hour
- D) 24 hours
- E) Cannot be determined from the document

**d03.q5** How many servers are reported as failed?
- A) 2
- B) 3
- C) 4
- D) 5
- E) Cannot be determined from the document

**d03.q6** Which of these servers has the latest-dated direct observation of its own state?
- A) node08
- B) node22
- C) node15
- D) node09
- E) Cannot be determined from the document

**d03.q7** For which server does the log explicitly say the status could not be determined?
- A) node15
- B) node11
- C) node07
- D) node14
- E) Cannot be determined from the document

**d03.q8** Which server was observed to be busy by opsbot?
- A) node09
- B) node08
- C) node11
- D) node23
- E) Cannot be determined from the document

**d03.q9** What did ops order for the job etl?
- A) To destroy it irreversibly (kill)
- B) To pause it so that it can be resumed (halt)
- C) To start it (run)
- D) Only to report its status (a request)
- E) Cannot be determined from the document

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

### Questions d04

**d04.q1** Which source reported that delta failed?
- A) mon
- B) opsbot
- C) auditor
- D) sre
- E) Cannot be determined from the document

**d04.q2** How is the claim that juliet being busy caused the failure of india classified?
- A) Inferred by mon, 90% confidence
- B) Inferred by mon, 80% confidence
- C) Inferred by sre, 90% confidence
- D) Directly observed by mon
- E) Cannot be determined from the document

**d04.q3** What confidence did the forecast for echo carry?
- A) 90%
- B) 95%
- C) 80%
- D) 55%
- E) Cannot be determined from the document

**d04.q4** Within what time span is juliet predicted to be full?
- A) 30 minutes
- B) 2 hours
- C) 1 hour
- D) 24 hours
- E) Cannot be determined from the document

**d04.q5** How many servers are reported as failed?
- A) 4
- B) 2
- C) 3
- D) 5
- E) Cannot be determined from the document

**d04.q6** Which of these servers has the latest-dated direct observation of its own state?
- A) hotel
- B) india
- C) echo
- D) juliet
- E) Cannot be determined from the document

**d04.q7** For which server does the log explicitly say the status could not be determined?
- A) bravo
- B) alpha
- C) hotel
- D) golf
- E) Cannot be determined from the document

**d04.q8** Which server was observed to be busy by sre?
- A) delta
- B) juliet
- C) alpha
- D) bravo
- E) Cannot be determined from the document

**d04.q9** What did ops order for the job cleanup?
- A) To destroy it irreversibly (kill)
- B) To pause it so that it can be resumed (halt)
- C) To start it (run)
- D) Only to report its status (a request)
- E) Cannot be determined from the document

