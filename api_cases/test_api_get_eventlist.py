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
from utils.commlib import get_test_data, get_data_from_database, echo_hd5

rootdir = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
yaml_data_file = os.path.join(rootdir,
                              'data\\data_api_get_eventlist.yaml')
ids, test_datas = get_test_data(yaml_data_file)


class Test_API_get_eventlist(object):
    @pytest.mark.parametrize('case, http, expected', test_datas, ids=ids)
    def test_get_eventlist(self, env, get_key_uid, case, http, expected):
        api_config = env
        host = api_config.get_config_data('host', 'url') + http['path']
        method = http['method']
        if get_key_uid:
            key_id, uid = get_key_uid
        else:
            print('can not get key and uid,test terminate!!!')
            assert False
        # print('########### login key_id is {}, uid is {} '.format(key_id, uid))
        headers = http['headers']
        params = http['params']
        headers['uid'] = uid if headers['uid'] == 'input' else '111'
        key_id = echo_hd5(uid, params['rstr'], key_id)
        headers['key'] = key_id if headers['key'] == 'input' else '111'
        # print('########### headers key_id is {}, uid is {} '.format(headers['uid'], headers['key']))
        r = requests.request(method=method,
                             url=host,
                             headers=headers,
                             params=params)
        response = r.json()
        print(response)
        with assume:
            assert r.status_code == expected['response']['status_code']
            assert response["error_code"] == expected['response']['error_code']
        if expected['data']:
            sql = expected['data']['sql'].format(title=params['title'], type=params['type'], price=200, status=0)
            print('########### sql is: ', sql)
            event_lists = get_data_from_database(os.path.join(rootdir, 'db.sqlite3'), sql)
            event_list = []
            for t in event_lists:
                event_list.append(t[1])
            print('########### event_list', event_list)
            assert response["count"] == len(response["event_list"]), "返回信息中的count与event_list中一致"
            for event in response["event_list"]:
                assert event['title'] in event_list, "返回信息中的event_list与预期一致"


if __name__ == "__main__":
    pytest.main(['-v', '-s', '--env', 'normal'])
