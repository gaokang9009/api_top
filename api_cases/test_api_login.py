#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：test of login interface
"""
import pytest
import requests
from pytest import assume


data_1 = [('', 'MTIzMmFkbWlu', 10001), ('gao', 'MTIzMmFkbWlu', 10000), ('gaokang', 'MTIzYWRtaW4=', 0),
          pytest.param("admin", 'admin', 0, marks=pytest.mark.xfail(reason='first xfail info')),
          pytest.param('caiying', 'MTIzYWRtaW4=', 0, marks=pytest.mark.skip(reason='just test skip'))]
ids = ["username:'{}' ,password:'{}' login device, expect error_code:'{}'".format(a, b, expect) for a, b, expect in data_1]


class Test_API_login(object):
    def test_login(self, env):
        api_config = env
        host = api_config.get_config_data('host', 'url')
        username = api_config.get_config_data('login', 'username')
        print(host, username)

    @pytest.mark.parametrize('username,password,expect_code', data_1, ids=ids)
    def test_login1(self, env, username, password, expect_code):
        api_config = env
        host = api_config.get_config_data('host', 'url') + '/event/api/login/'
        print(host)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/80.0.3987.149 Safari/537.36"
        }
        data = {
            "username": username,
            "password": password
        }
        r = requests.post(url=host,
                          headers=headers,
                          data=data)
        response = r.json()
        assert response["error_code"] == expect_code
        if response["error_code"] == 0:
            with assume:
                assert response["token"] == '9d5eb3bdaf6a3c20ae7db90c4161b602211115f1#', "返回信息中的token与预期一致"
            assert response["token"] == '9d5eb3bdaf6a3c20ae7db90c4161b602211115f1', "返回信息中的token与预期一致"
            assert response["uid"] == 2, "返回信息中的uid与预期一致"


if __name__ == "__main__":
    pytest.main(['-v', '-s', '--env', 'super'])
