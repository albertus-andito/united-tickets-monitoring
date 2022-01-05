mkdir -p logs
nohup ./united-tickets-monitoring-venv/bin/python ./united-tickets-monitoring/database_watcher.py >/dev/null 2>> ./logs/database-watcher.log &
nohup ./united-tickets-monitoring-venv/bin/python ./united-tickets-monitoring/poller.py >/dev/null 2>> ./logs/poller.log &