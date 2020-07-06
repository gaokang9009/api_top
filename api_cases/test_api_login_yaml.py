#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：test of login interface
"""
import os
import base64
import pytest
import requests
from pytest import assume
from utils.commlib import get_test_data, get_data_from_database

# os.path.relpath()
# yaml_data_file = '.\\data\\data_api_login.yaml'
yaml_data_file = os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), 'data\\data_api_login.yaml')
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
            sql = "SELECT authtoken_token.key,auth_user.username from authtoken_token \
                                inner join auth_user on  authtoken_token.user_id=auth_user.id \
                                where auth_user.username='{}'".format(http['params']['username'])
            tokens = get_data_from_database('.\\db.sqlite3', sql)
            token = ''
            for t in tokens:
                token = t[0]
            assert response["token"] == token, "返回信息中的token与预期一致"


if __name__ == "__main__":
    pytest.main(['-v', '-s', '--env', 'normal'])
