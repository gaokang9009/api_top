#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：
pytest conftest
"""

import base64
import os
import pytest
import requests
from utils.commlib import ApiConfig


def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     dest="environment",
                     default="normal",
                     help="environment: normal or super")


@pytest.fixture(scope="session")
def env(request):
    environment = request.config.getoption('environment')
    config_dir = 'config_super' if environment == "super" else "config_normal"
    config_path = os.path.join(request.config.rootdir,
                               "config",
                               config_dir,
                               "config.ini")
    api_config = ApiConfig(config_path)
    return api_config


@pytest.fixture(scope='module')
def get_key_uid(env):
    api_config = env
    username = api_config.get_config_data('login', 'username')
    password_original = api_config.get_config_data('login', 'password')
    key_id = api_config.get_config_data('authentication', 'key_id')
    uid = api_config.get_config_data('authentication', 'uid')
    host = api_config.get_config_data('login', 'login_url')
    print('\r\nlogin info is: ', host, username, password_original, key_id, uid)
    password = base64.b64encode(bytes('123' + password_original, 'utf-8'))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/83.0.4103.106 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        "username": username,
        "password": password
    }
    r = requests.post(url=host,
                      headers=headers,
                      data=data)
    response = r.json()
    print('########### login response :', response)
    try:
        key_id_status = api_config.add_config_data('authentication', 'key_id', response['token'])
        uid_status = api_config.add_config_data('authentication', 'uid', str(response['uid']))
    except Exception as e:
        print('write config of {}\'file failed, {}'.format(api_config.get_config_data('description', 'environment'), e))
    else:
        return response['token'], str(response['uid']) if key_id_status and uid_status else False


