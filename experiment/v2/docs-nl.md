# Documents (plain English)

Four incident logs. Questions are provided separately.

---

## d01

Incident log d01.

According to mon (at 1730501197), db3 is idle. According to opsbot (at 1730500819), queue2 is healthy. According to auditor (at 1730501106), db1 is busy. According to sre (at 1730502751), web2 has failed. sre reported at 1730500728 that cache1 has failed.

sre reported at 1730500637 that queue1 has failed. mon reported at 1730500504 that cache2 is busy. At 1730500672, sre observed that web3 has failed. At 1730500749, mon estimated, with 55% confidence, that cache2 will be full within 2 hours. At 1730501652, ops ordered the job backup to be halted, meaning paused so that it can be resumed later.

At 1730501463, opsbot inferred, with 85% confidence, that cache2 being busy caused the failure of cache1. sre concluded at 1730502240, with 90% confidence, that db1 being busy caused the failure of web2. At 1730501988, ops ordered the job etl to be killed, meaning destroyed irreversibly. At 1730500987, the worker acknowledged receiving the order to halt backup; it did not say whether the job was halted. At 1730501442, sre estimated, with 80% confidence, that db1 will be full within 30 minutes.

At 1730501239, sre could not determine whether db2 is healthy. At 1730501323, auditor could not determine whether web1 is healthy. At 1730502989, auditor inferred, with 95% confidence, that the failure of web2 caused an SLA breach.

---

## d02

Incident log d02.

According to mon (at 1730510315), gw-ap has failed. At 1730511589, sre observed that gw-us is healthy. At 1730512758, mon observed that auth2 is busy. According to sre (at 1730511925), gw-eu is healthy. According to mon (at 1730511309), search2 has failed.

sre reported at 1730510686 that pay1 was deliberately stopped. At 1730511687, opsbot observed that auth1 has failed. At 1730512814, opsbot observed that ml1 is busy. At 1730510854, auditor could not determine whether search1 is healthy. At 1730511540, ops ordered the job report to be killed, meaning destroyed irreversibly.

sre concluded at 1730512282, with 55% confidence, that auth2 being busy caused the failure of gw-ap. auditor concluded at 1730512835, with 85% confidence, that ml1 being busy caused the failure of search2. At 1730511442, opsbot inferred, with 60% confidence, that the failure of gw-ap caused an SLA breach. opsbot said at 1730511162 that it does not know whether pay2 is healthy. At 1730510742, mon estimated, with 95% confidence, that gw-eu will be full within 30 minutes.

At 1730510224, ops ordered the job etl to be halted, meaning paused so that it can be resumed later. At 1730511512, mon estimated, with 65% confidence, that ml1 will be full within 2 hours. At 1730511673, the worker acknowledged receiving the order to halt etl; it did not say whether the job was halted.

---

## d03

Incident log d03.

At 1730521582, opsbot observed that node11 was deliberately stopped. mon reported at 1730520812 that node08 has failed. opsbot reported at 1730521827 that node15 has failed. At 1730520455, sre observed that node22 has failed. According to auditor (at 1730520301), node12 is healthy.

At 1730522898, opsbot observed that node23 is busy. At 1730520189, auditor observed that node14 is busy. According to opsbot (at 1730522471), node09 has failed. At 1730520791, sre estimated, with 65% confidence, that node14 will be full within 1 hour. At 1730522555, mon estimated, with 85% confidence, that node12 will be full within 2 hours.

auditor said at 1730522177 that it does not know whether node21 is healthy. At 1730521883, ops ordered the job etl to be killed, meaning destroyed irreversibly. At 1730521792, auditor inferred, with 90% confidence, that node14 being busy caused the failure of node15. At 1730521897, ops ordered the job reindex to be halted, meaning paused so that it can be resumed later. At 1730520658, auditor could not determine whether node07 is healthy.

At 1730522996, opsbot inferred, with 80% confidence, that the failure of node08 caused an SLA breach. opsbot concluded at 1730522058, with 95% confidence, that node23 being busy caused the failure of node08. At 1730520518, the worker acknowledged receiving the order to halt reindex; it did not say whether the job was halted.

---

## d04

Incident log d04.

According to sre (at 1730530378), juliet is busy. At 1730532478, auditor observed that india has failed. According to opsbot (at 1730530455), alpha has failed. At 1730532170, opsbot observed that foxtrot is healthy. At 1730531869, mon observed that echo is busy.

auditor reported at 1730531050 that bravo has failed. At 1730530651, sre observed that delta has failed. According to mon (at 1730532667), hotel is idle. At 1730532814, ops ordered the job reindex to be halted, meaning paused so that it can be resumed later. At 1730532590, mon inferred, with 80% confidence, that echo being busy caused the failure of alpha.

At 1730531484, auditor estimated, with 95% confidence, that echo will be full within 24 hours. At 1730532408, auditor inferred, with 55% confidence, that the failure of india caused an SLA breach. At 1730532352, ops ordered the job cleanup to be killed, meaning destroyed irreversibly. sre said at 1730531463 that it does not know whether golf is healthy. At 1730530812, auditor estimated, with 85% confidence, that juliet will be full within 2 hours.

At 1730532051, the worker acknowledged receiving the order to halt reindex; it did not say whether the job was halted. At 1730532079, mon inferred, with 90% confidence, that juliet being busy caused the failure of india. auditor said at 1730532625 that it does not know whether charlie is healthy.

