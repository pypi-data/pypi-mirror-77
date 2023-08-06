# -*- coding: utf-8 -*-

import os
from awsvault import Vault


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    AWS_SECRETS = os.getenv('AWS_SECRETS')
    vault = Vault([s.strip() for s in AWS_SECRETS.split(',')] if AWS_SECRETS else [])

    AWS_ENDPOINT_URL = vault.get('AWS_ENDPOINT_URL')

    BROKER_URL = vault.get("BROKER_URL")
    RESULT_BACKEND_URL = vault.get("RESULT_BACKEND_URL")
    WAVES_URL = vault.get("WAVES_URL")
    WAVES_RESULTS_PATH = vault.get('WAVES_RESULTS_PATH', 'waves/results')

    WAVES_CLI_NAME = os.getenv('WAVES_CLI_NAME', 'waves')
    QUEUE_NAME = os.getenv('QUEUE_NAME', 'waves_latest')
    BROKER_HEARTBEAT = os.getenv('BROKER_HEARTBEAT', None)
    BROKER_CONNECTION_TIMEOUT = os.getenv('BROKER_CONNECTION_TIMEOUT', 30)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


def get_config(env='prod'):

    if env in ['development', 'dev']:
        return DevelopmentConfig()

    return ProductionConfig()
