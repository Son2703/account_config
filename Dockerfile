FROM python:3.8

WORKDIR /home/mobio/projects/AccountConfig

COPY requirements.txt /home/mobio/projects/AccountConfig

RUN pip3.8 install -r requirements.txt

ENV LC_ALL=en_US.UTF-8 \
   ACCOUNT_CONFIG_HOME=/home/mobio/projects/AccountConfig \
   ACCOUNT_CONFIG_FOLDER_NAME=AccountConfig \
   APPLICATION_DATA_DIR=/media/data/resources/ \
   APPLICATION_LOGS_DIR=/media/data/logs/daily/

ENV data_dir=$APPLICATION_DATA_DIR$ACCOUNT_CONFIG_FOLDER_NAME \
   log_dir=$APPLICATION_LOGS_DIR$ACCOUNT_CONFIG_FOLDER_NAME \
   monitor_log_dir=$APPLICATION_LOGS_DIR$ACCOUNT_CONFIG_FOLDER_NAME/monitor_logs/

RUN mkdir -p $data_dir $log_dir $monitor_log_dir

ADD . /home/mobio/projects/AccountConfig

RUN chmod +x *.sh

CMD ["python3", "app_account_config_api.py"]

EXPOSE 8000