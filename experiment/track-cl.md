# Comprehension experiment, track CL

The eight documents below are written in CL (Concept Language). Each is followed by its questions. CL is defined by SPEC.md and lexicon.json.

---

## s01 - Server report

```cl
#t=1730415600
@1 obs sys:srv1 has fail src=mon
@2 obs res:mem has full src=mon
@3 obs res:cpu has busy src=mon
@4 inf @2 cause @1 conf=.8 src=opsbot
@5 obs @3 corr @1 src=mon
```

### Questions s01

**s01.q1** How is the claim that full memory caused the failure classified in the report?
- A) Inferred by the analysis bot, not directly observed
- B) Directly observed by the monitor
- C) A forecast of a future event
- D) Stated as unknown
- E) Cannot be determined from the document

**s01.q2** What does the report claim about the CPU load and the failure?
- A) The CPU load caused the failure
- B) They occurred together; no causal claim is made
- C) The CPU load probably caused the failure
- D) The CPU load was ruled out as a cause
- E) Cannot be determined from the document

**s01.q3** Who made the causal claim, and with what confidence?
- A) mon, 80%
- B) opsbot, 95%
- C) mon, 100% (observed)
- D) opsbot, 80%
- E) Cannot be determined from the document

**s01.q4** How is the statement that memory was full classified?
- A) Inferred by the analysis bot
- B) A forecast of a future event
- C) Directly observed by the monitor
- D) Stated as unknown
- E) Cannot be determined from the document

---

## s02 - Cluster health

```cl
#src=deploybot t=1730420000
obs all.sys:web has ok
obs some.sys:db has fail
obs sys:db2 has fail
obs sys:db1 has ok
obs none.sys:cache has fail
unk sys:queue has ok
```

### Questions s02

**s02.q1** What is stated about the web servers?
- A) At least one is healthy; the others are not specified
- B) All of them are healthy
- C) None of them is healthy
- D) Nothing is stated about them
- E) Cannot be determined from the document

**s02.q2** Did any cache server fail?
- A) Yes, all of them failed
- B) No, none of them failed
- C) Yes, some of them failed
- D) It is unknown
- E) Cannot be determined from the document

**s02.q3** Which database server is stated to have failed?
- A) db1 only
- B) both db1 and db2
- C) neither of them
- D) db2 only
- E) Cannot be determined from the document

**s02.q4** What is stated about the queue system?
- A) It is healthy
- B) It failed
- C) The reporter explicitly could not determine whether it is healthy
- D) The queue system is not mentioned at all
- E) Cannot be determined from the document

---

## s03 - Job control

```cl
#t=1730421000
@1 cmd proc:job1 do halt src=ops
@2 ack @1 to agent:worker src=worker
@3 obs proc:job2 has fail src=worker
@4 obs proc:job3 has stop src=worker
@5 cmd proc:job4 do kill src=ops
```

### Questions s03

**s03.q1** Which job experienced an unplanned malfunction?
- A) job2
- B) job1
- C) job3
- D) job4
- E) Cannot be determined from the document

**s03.q2** What happened to job3?
- A) It failed unexpectedly
- B) It was ordered to be destroyed
- C) It was deliberately stopped
- D) It was ordered to be paused
- E) Cannot be determined from the document

**s03.q3** Has the worker confirmed that job1 was actually halted?
- A) No, it only acknowledged receiving the order
- B) Yes, the job is halted
- C) No, the worker refused the order
- D) The order was never sent
- E) Cannot be determined from the document

**s03.q4** How do the orders for job1 and job4 differ?
- A) The order for job1 destroys the job; the order for job4 can be undone
- B) They are identical
- C) The order for job4 is only a request for information
- D) The order for job1 can be undone (it can resume); the order for job4 destroys the job irreversibly
- E) Cannot be determined from the document

---

## s04 - Latency timeline

```cl
obs event:deploy bef event:spike src=mon t=1730430100
obs event:cert_expiry bef event:spike src=mon t=1730430100
obs event:spike bef event:rollback src=ops t=1730430400
inf event:deploy cause event:spike conf=.6 src=sre t=1730430500
unk event:cert_expiry cause event:spike src=sre t=1730430500
```

### Questions s04

**s04.q1** Which order of events is stated for the deploy, the spike and the rollback?
- A) Spike, then deploy, then rollback
- B) Rollback, then deploy, then spike
- C) Deploy, then rollback, then spike
- D) Deploy, then spike, then rollback
- E) Cannot be determined from the document

**s04.q2** What does the report establish about the deploy causing the spike?
- A) sre inferred it with 60% confidence; it was not directly observed
- B) It was directly observed by mon
- C) It is ruled out
- D) It is stated as certain
- E) Cannot be determined from the document

**s04.q3** What is stated about whether the certificate expiry caused the spike?
- A) It caused the spike with certainty
- B) sre explicitly states that this is unknown
- C) It probably caused the spike (60%)
- D) It was ruled out
- E) Cannot be determined from the document

**s04.q4** Who reported that the spike happened before the rollback?
- A) mon
- B) ops
- C) sre
- D) Nobody reported it
- E) Cannot be determined from the document

---

## s05 - Capacity status

```cl
#t=1730435000
obs rule:alert_threshold has val:90 unit=pct src=cfg
obs res:cpu has val:92 unit=pct src=s3
obs res:disk has val:83 unit=pct src=s3
est res:disk has val:95 unit=pct conf=.65 dur=86400 src=planner
```

### Questions s05

**s05.q1** Which resources currently exceed the alert threshold?
- A) Disk only
- B) CPU only
- C) Both CPU and disk
- D) Neither of them
- E) Cannot be determined from the document

**s05.q2** Which statement correctly describes the disk forecast?
- A) Observed 83 percent
- B) Estimated 83 percent, with 95% confidence
- C) Inferred 95 percent, with 65% confidence
- D) Estimated 95 percent, with 65% confidence
- E) Cannot be determined from the document

**s05.q3** Over what time span does the forecast apply?
- A) 1 hour
- B) 7 days
- C) 24 hours
- D) 90 minutes
- E) Cannot be determined from the document

**s05.q4** Which source supplied the current CPU reading?
- A) s3
- B) cfg
- C) planner
- D) It is not stated
- E) Cannot be determined from the document

---

## s06 - Pipeline report

```cl
#t=1730440000
@1 obs data:feed has null src=ingest
@2 obs store:table1 has empty src=ingest
@3 inf proc:report has fail conf=.9 src=etl
@4 inf @1 cause @3 conf=.9 src=etl
@5 inf @3 cause event:sla_breach conf=.6 src=etl
```

### Questions s06

**s06.q1** What is the state of the feed?
- A) It is present but contains zero records
- B) It failed
- C) It has no value at all (the value is absent)
- D) It was deliberately stopped
- E) Cannot be determined from the document

**s06.q2** What is stated about table1?
- A) Its value is absent
- B) It is full
- C) It exists and contains zero rows
- D) It failed
- E) Cannot be determined from the document

**s06.q3** How is the SLA breach claim supported?
- A) Directly observed by ingest
- B) Inferred with 90% confidence directly from the empty table
- C) Estimated as a forecast by ingest with 60% confidence
- D) Inferred by etl with 60% confidence, as a consequence of the report failure
- E) Cannot be determined from the document

**s06.q4** How many statements in the report are direct observations?
- A) One
- B) Three
- C) Five
- D) Two
- E) Cannot be determined from the document

---

## s07 - Billing request

```cl
req sys:billing has ok src=support t=1730445000
obs sys:billing has busy src=billmon t=1730445060
cmd data:export_q3 to store:archive src=ops t=1730445100
obs data:export_q3 has valid src=validator t=1730445200
unk data:export_q3 has true src=validator t=1730445200
```

### Questions s07

**s07.q1** What did support do in its message?
- A) It reported that billing is healthy
- B) It asked a question about the health of billing
- C) It ordered billing to restart
- D) It observed that billing was healthy
- E) Cannot be determined from the document

**s07.q2** What state is billing reported to be in?
- A) Healthy and idle
- B) Failed
- C) Busy (fully engaged), not failing
- D) Deliberately stopped
- E) Cannot be determined from the document

**s07.q3** What does the validator state about export_q3?
- A) It is valid and also confirmed correct
- B) It conforms to the rules (valid), but whether it is correct is unknown
- C) It is invalid
- D) Whether it is valid is unknown
- E) Cannot be determined from the document

**s07.q4** What kind of thing is the destination in the order from ops?
- A) A person or a program
- B) A running process
- C) A network link
- D) A storage container (the archive)
- E) Cannot be determined from the document

---

## s08 - Combined incident

```cl
#t=1730450000
@1 obs sys:api has fail src=mon
obs sys:auth has ok src=mon
@3 obs sys:db has busy src=mon
inf @3 cause @1 conf=.7 src=sre
inf sys:auth cause @1 conf=.05 src=sre
est sys:db has full conf=.6 dur=3600 src=sre
cmd proc:cleanup do run src=ops
unk proc:retry has ok src=mon
```

### Questions s08

**s08.q1** According to whom, and in what way, is the busy database the cause of the API failure?
- A) sre, inferred with 70% confidence
- B) mon, directly observed
- C) sre, a forecast with 60% confidence
- D) ops, given as an order
- E) Cannot be determined from the document

**s08.q2** What does the report say about auth as a possible cause of the API failure?
- A) sre judged it a very unlikely cause (about 5%)
- B) sre judged it the most likely cause
- C) mon observed that auth caused the failure
- D) Auth is not mentioned as a possible cause
- E) Cannot be determined from the document

**s08.q3** What is predicted for the database within the next hour, and with what confidence?
- A) It will fail, with 70% confidence
- B) It will be busy, with 60% confidence
- C) It will be full, with 60% confidence
- D) It is already full (observed)
- E) Cannot be determined from the document

**s08.q4** Which of these is explicitly stated as unknown?
- A) Whether the retry process succeeded
- B) Whether the API failed
- C) Whether auth is healthy
- D) Whether the database is busy
- E) Cannot be determined from the document

