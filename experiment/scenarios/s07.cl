req sys:billing has ok src=support t=1730445000
obs sys:billing has busy src=billmon t=1730445060
cmd data:export_q3 to store:archive src=ops t=1730445100
obs data:export_q3 has valid src=validator t=1730445200
unk data:export_q3 has true src=validator t=1730445200
