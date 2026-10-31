#t=1730415600
@1 obs sys:srv1 has fail src=mon
@2 obs res:mem has full src=mon
@3 obs res:cpu has busy src=mon
@4 inf @2 cause @1 conf=.8 src=opsbot
@5 obs @3 corr @1 src=mon
