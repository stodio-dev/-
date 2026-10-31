#t=1730440000
@1 obs data:feed has null src=ingest
@2 obs store:table1 has empty src=ingest
@3 inf proc:report has fail conf=.9 src=etl
@4 inf @1 cause @3 conf=.9 src=etl
@5 inf @3 cause event:sla_breach conf=.6 src=etl
