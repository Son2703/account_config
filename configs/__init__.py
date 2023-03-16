#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from mobio.sdks.base.configs import ApplicationConfig


class AccountConfigApplicationConfig(ApplicationConfig):
    NAME = 'AccountConfig'

    ApplicationConfig.WORKING_DIR = str(os.environ.get("ACCOUNT_CONFIG_HOME"))
    ApplicationConfig.RESOURCE_DIR = os.path.join(ApplicationConfig.WORKING_DIR, 'resources')
    ApplicationConfig.CONFIG_DIR = os.path.join(ApplicationConfig.RESOURCE_DIR, 'configs')
    ApplicationConfig.LANG_DIR = os.path.join(ApplicationConfig.RESOURCE_DIR, 'lang')

    ApplicationConfig.CONFIG_FILE_PATH = os.path.join(ApplicationConfig.CONFIG_DIR, 'account_config.conf')
    ApplicationConfig.LOG_CONFIG_FILE_PATH = os.path.join(ApplicationConfig.CONFIG_DIR, 'logging.conf')
    ApplicationConfig.LOG_FILE_PATH = os.path.join(ApplicationConfig.APPLICATION_LOGS_DIR)

    ACCOUNT_CONFIG_FOLDER_NAME = os.environ.get('ACCOUNT_CONFIG_FOLDER_NAME')

    ADMIN_HOST = os.environ.get("ADMIN_HOST", '')


class RedisConfig:
    REDIS_URI = os.environ.get('REDIS_URI', 'redis://redis-server:6379/0')
