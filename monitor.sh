#!/usr/bin/bash

send_data() {
  data=$1
  machine=$(hostname)
  curl -X POST -H  "Content-Type: text/plain" --fail-with-body  --data-binary "$data
"  http://localhost:9091/metrics/job/top/instance/$machine
  if [ $? -ne 0 ]; then
    echo "Failed to send metrics"
  fi
}

data=$(ps aux | awk 'NR>1{
    print "cpu_usage{process=\""$11"\",pid=\""$2"\"} "$3"\n" \
          "memory_usage{process=\""$11"\",pid=\""$2"\"} "$4"\n" \
          "virt_mem{process=\""$11"\",pid=\""$2"\"} "$5"\n" \
          "res_mem{process=\""$11"\",pid=\""$2"\"} "$6
}')

send_data "$data"



#curl -X POST -H  "Content-Type: text/plain" --data-binary "$virt_mem
#" http://localhost:9091/metrics/job/top/instance/$machine
#
#curl -X POST -H  "Content-Type: text/plain" --data-binary "$res_mem
#" http://localhost:9091/metrics/job/top/instance/$machine

#curl -X POST -H  "Content-Type: text/plain" --data-binary "$time
#" http://localhost:9091/metrics/job/top/instance/$machine
