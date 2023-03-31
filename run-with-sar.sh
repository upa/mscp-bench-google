#!/bin/bash
#
# Execut mscp with sysstat

sar_cmd="sar -o sysstat.sar 1"

# start sar on local
$sar_cmd > /dev/null 2>&1 &
sar_pid=$!

$@

# stop sar
kill -INT $sar_pid
sleep 1
if [ -e /proc/$sar_pid ]; then
	kill -KILL $sar_pid
fi
