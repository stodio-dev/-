#t=1730421000
@1 cmd proc:job1 do halt src=ops
@2 ack @1 to agent:worker src=worker
@3 obs proc:job2 has fail src=worker
@4 obs proc:job3 has stop src=worker
@5 cmd proc:job4 do kill src=ops
