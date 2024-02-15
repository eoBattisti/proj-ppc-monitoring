#!/usr/bin/bash

send_data() {
  data=$1
  machine=$(hostname)
  curl -X POST -H  "Content-Type: text/plain" --silent --fail-with-body  --data-binary "$data
"  http://localhost:9091/metrics/job/top/instance/$machine
  if [ $? -ne 0 ]; then
    echo "[ERROR][$(date +%Y-%m-%dT%H:%M:%S)]: Failed to send metrics to pushgateway"
    python3 ./client/producer/main.py --data "$data" --machine "$machine"
    exit 1
  else
    echo "[INFO][$(date +%Y-%m-%dT%H:%M:%S)]: Successfully sent metrics to pushgateway"
  fi
}

data=$(ps aux | awk 'NR>1{
    # Convert mm:ss to total seconds
    split($10, time_parts, ":")
      if (length(time_parts) == 3) {
          # Format: hh:mm:ss
          days = 0
          hours = time_parts[1]
          minutes = time_parts[2]
          seconds = time_parts[3]
      } else if (length(time_parts) == 4) {
          # Format: DD-hh:mm:ss
          days = time_parts[1]
          hours = time_parts[2]
          minutes = time_parts[3]
          seconds = time_parts[4]
      } else {
          # Default to mm:ss
          days = 0
          hours = 0
          minutes = time_parts[1]
          seconds = time_parts[2]
      }

    # Calculate total seconds
    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
    print "cpu_usage{process=\""$11"\",pid=\""$2"\"} "$3"\n" \
          "memory_usage{process=\""$11"\",pid=\""$2"\"} "$4"\n" \
          "virt_mem{process=\""$11"\",pid=\""$2"\"} "$5"\n" \
          "res_mem{process=\""$11"\",pid=\""$2"\"} "$6"\n" \
          "time{process=\""$11"\",pid=\""$2"\"} "total_seconds""
}')

send_data "$data"
