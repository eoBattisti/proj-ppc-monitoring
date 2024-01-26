#!/usr/bin/bash


if [ -e /etc/systemd/system/pcmonitoring.service ]; then
  echo "Stopping third party service - Process Monitoring Service"
  sudo systemctl stop pcmonitoring
fi

echo "Registering third party service - Process Monitoring Service"
sudo cp monitor.sh /usr/local/bin/monitor.sh
sudo cp pcmonitoring.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pcmonitoring
sudo systemctl start pcmonitoring

echo "Reloading systemd daemon"
sudo systemctl daemon-reload

