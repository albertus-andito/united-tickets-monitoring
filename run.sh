mkdir -p logs
nohup ./united-tickets-monitoring-venv/bin/python ./united-tickets-monitoring/database_watcher.py > ./logs/database-watcher.log &
nohup ./united-tickets-monitoring-venv/bin/python ./united-tickets-monitoring/poller.py > ./logs/poller.log &