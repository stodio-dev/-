#t=1730435000
obs rule:alert_threshold has val:90 unit=pct src=cfg
obs res:cpu has val:92 unit=pct src=s3
obs res:disk has val:83 unit=pct src=s3
est res:disk has val:95 unit=pct conf=.65 dur=86400 src=planner
