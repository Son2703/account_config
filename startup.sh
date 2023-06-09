#!/bin/bash

data_dir=$APPLICATION_DATA_DIR$ACCOUNT_CONFIG_FOLDER_NAME
log_dir=$APPLICATION_LOGS_DIR$ACCOUNT_CONFIG_FOLDER_NAME
monitor_log_dir=$APPLICATION_LOGS_DIR$ACCOUNT_CONFIG_FOLDER_NAME/monitor_logs/

if [[ ! -d $data_dir ]];then
    echo "data dir $data_dir"
    mkdir -p $data_dir
fi

if [[ ! -d $log_dir ]];then
    echo "data dir $log_dir"
    mkdir -p $log_dir
fi

if [[ ! -d $monitor_log_dir ]]; then
    echo "monitor logs dir: $monitor_log_dir"
    mkdir -p $monitor_log_dir
fi

echo "app api"
nohup uwsgi --http :80 --wsgi-file app_account_config_api.py --callable app --master --processes 4 -b 65536 --lazy --enable-threads -l 100 >> $log_dir/api.out 2>&1 &