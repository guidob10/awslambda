## Process:

The objetive of this function is to enable/disable with disable_alarm_actions/enable_alarm_actions some
of the alarms that we have in cloudwatch. The idea is to stop the notifications while the instances are running
some maintaining task at night, so we have to set a cron in cloudwatch events (Amazon EventBridge) to trigger at certain time the function.
For example: cron(30 3 * * ? *) will run at 3.30 everyday.