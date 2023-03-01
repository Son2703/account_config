FROM BE_BASE_COMPILE_IMAGE as compile-image

WORKDIR /home/mobio/projects/AccountConfig
ADD . /home/mobio/projects/AccountConfig

RUN pip3.8 install -r requirements.txt

FROM BE_BASE_RUN_IMAGE as run-image

ENV LC_ALL=en_US.UTF-8 \
   ACCOUNT_CONFIG_HOME=/home/mobio/projects/AccountConfig \
   ACCOUNT_CONFIG_FOLDER_NAME=AccountConfig \
   APPLICATION_DATA_DIR=/media/data/resources/ \
   APPLICATION_LOGS_DIR=/media/data/logs/daily/

ENV data_dir=$APPLICATION_DATA_DIR$ACCOUNT_CONFIG_FOLDER_NAME \
   log_dir=$APPLICATION_LOGS_DIR$ACCOUNT_CONFIG_FOLDER_NAME \
   monitor_log_dir=$APPLICATION_LOGS_DIR$ACCOUNT_CONFIG_FOLDER_NAME/monitor_logs/

RUN mkdir -p $data_dir $log_dir $monitor_log_dir

WORKDIR $ACCOUNT_CONFIG_HOME

COPY --from=compile-image $ACCOUNT_CONFIG_HOME $ACCOUNT_CONFIG_HOME

COPY --from=compile-image /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=compile-image /usr/local/bin/uwsgi /usr/local/bin/uwsgi

RUN chmod +x *.sh

CMD tail -f /dev/null