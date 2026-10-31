#t=1730450000
@1 obs sys:api has fail src=mon
obs sys:auth has ok src=mon
@3 obs sys:db has busy src=mon
inf @3 cause @1 conf=.7 src=sre
inf sys:auth cause @1 conf=.05 src=sre
est sys:db has full conf=.6 dur=3600 src=sre
cmd proc:cleanup do run src=ops
unk proc:retry has ok src=mon
