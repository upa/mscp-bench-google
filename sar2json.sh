#!/bin/bash -xeu

for f in $(find $1 | grep sar$ ); do
	echo $f
	sadf -t -j $f -- -P ALL -u ALL > ${f}.cpu.json
	sadf -t -j $f -- -n DEV > ${f}.net.json
done

