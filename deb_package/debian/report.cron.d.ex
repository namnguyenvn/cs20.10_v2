#
# Regular cron jobs for the report package
#
0 4	* * *	root	[ -x /usr/bin/report_maintenance ] && /usr/bin/report_maintenance
