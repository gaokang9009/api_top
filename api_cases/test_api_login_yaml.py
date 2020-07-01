#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：test of login interface
"""
import base64
import pytest
import requests
from pytest import assume
from utils.commlib import get_test_data


yaml_data_file = '.\\data\\data_api_login.yaml'
ids, test_datas = get_test_data(yaml_data_file)


class Test_API_login(object):
    @pytest.mark.parametrize('case, http, expected', test_datas, ids=ids)
    def test_login(self, env, case, http, expected):
        api_config = env
        host = api_config.get_config_data('host', 'url') + http['path']
        method = http['method']
        headers = http['headers']
        if http['params']['password']:
            password = base64.b64encode(bytes('123' + http['params']['password'], 'utf-8'))
        else:
            password = ''
        data = {
            "username": http['params']['username'],
            "password": password
        }
        r = requests.request(method=method,
                             url=host,
                             headers=headers,
                             data=data)
        response = r.json()
        with assume:
            assert r.status_code == expected['response']['status_code']
            assert response["error_code"] == expected['response']['error_code']
        if response["error_code"] == 0 and http['params']['username'] == 'caiying':
            assert response["token"] == 'a63171bdf280c6033366bd1fb6ab66adc06b4027', "返回信息中的token与预期一致"


if __name__ == "__main__":
    pytest.main(['-v', '-s', '--env', 'super'])
