#!/usr/bin/bash
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

z=$(ps aux)
while read -r z
do
  virt_mem=$virt_mem$(awk '{print "virt_mem{process=\""$11"\", pid=\""$2"\"}", $5z}')
done <<< "$z"

z=$(ps aux)
while read -r z
do
  res_mem=$res_mem$(awk '{print "res_mem{process=\""$11"\", pid=\""$2"\"}", $6z}')
done <<< "$z"

z=$(ps aux)
while read -r z
do
  time=$time$(awk '{print "time{process=\""$11"\", pid=\""$2"\"}", $9z}');
done <<< "$z"

curl -X POST -H  "Content-Type: text/plain" --data-binary "$cpu
" http://localhost:9091/metrics/job/top/instance/$machine

curl -X POST -H  "Content-Type: text/plain" --data-binary "$mem
" http://localhost:9091/metrics/job/top/instance/$machine

curl -X POST -H  "Content-Type: text/plain" --data-binary "$virt_mem
" http://localhost:9091/metrics/job/top/instance/$machine

curl -X POST -H  "Content-Type: text/plain" --data-binary "$res_mem
" http://localhost:9091/metrics/job/top/instance/$machine

#curl -X POST -H  "Content-Type: text/plain" --data-binary "$time
#" http://localhost:9091/metrics/job/top/instance/$machine
