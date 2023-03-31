#!/bin/bash
#
# Execut command with sysstat

first=$1

echo $@ > command.txt

for x in $(seq 1 5); do

	sar_out=sysstat-${x}.sar
	dur_out=duration-${x}.txt

	# start sar on local
	sar -o $sar_out 1 > /dev/null 2>&1 &
	sar_pid=$!

	# save start time
	startat=$(cat /proc/uptime | awk '{print $1}')
	$@
	# save end time
	endat=$(cat /proc/uptime | awk '{print $1}')

	# stop sar
	kill -INT $sar_pid
	sleep 1
	if [ -e /proc/$sar_pid ]; then
		kill -KILL $sar_pid
	fi 

	# calculate duration
	echo "$endat - $startat" | bc > $dur_out

done
