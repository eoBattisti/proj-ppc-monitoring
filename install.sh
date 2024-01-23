#!/usr/bin/bash

# Copying the monitoring script
sudo cp monitor.sh /usr/local/bin/monitor.sh

# Install the service on the machine
if [ ! -e /etc/systemd/system/prometheus.service ]; then
  echo "Registering third party service - Process Monitoring Service"
  sudo cp pcmonitoring.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable pcmonitoring
  sudo systemctl start pcmonitoring
fi

# reload the daemon
sudo systemctl daemon-reload

