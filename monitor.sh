#!/usr/bin/bash
# TODO: Add a way to get uptime in seconds
machine=$(hostname)

z=$(ps aux)

while read -r z
do
  cpu=$cpu$(awk '{print "cpu_usage{process=\""$11"\", pid=\""$2"\"}", $3z}');
done <<< "$z"

z=$(ps aux)
while read -r z
do
  mem=$mem$(awk '{print "mem_usage{process=\""$11"\", pid=\""$2"\"}", $4z}');
done <<< "$z"

curl -X POST -H  "Content-Type: text/plain" --data-binary "$cpu
" http://localhost:9091/metrics/job/top/instance/$machine

curl -X POST -H  "Content-Type: text/plain" --data-binary "$mem
" http://localhost:9091/metrics/job/top/instance/$machine
