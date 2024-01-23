#!/usr/bin/bash

# Install the service on the machine
if [ ! -e /etc/systemd/system/prometheus.service ]; then
  sudo cp pcmonitoring.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable pcmonitoring
  sudo systemctl start pcmonitoring
fi
