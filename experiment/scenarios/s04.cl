obs event:deploy bef event:spike src=mon t=1730430100
obs event:cert_expiry bef event:spike src=mon t=1730430100
obs event:spike bef event:rollback src=ops t=1730430400
inf event:deploy cause event:spike conf=.6 src=sre t=1730430500
unk event:cert_expiry cause event:spike src=sre t=1730430500
