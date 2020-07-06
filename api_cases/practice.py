#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：test of login interface
"""
import os
from utils.commlib import get_config_data1, add_config_data1,get_test_data
import sqlite3
import hashlib

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                           'config\\config_normal\\config.ini')
# cases, list_params = get_test_data("/Users/chunming.liu/learn/api_pytest/data/test_in_theaters.yaml")
host = get_config_data1(config_path, 'host', 'url')

# def get_test_data(test_data_path):
#     case = []  # 测试用例名称
#     http = []  # 请求对象
#     expected = []  # 预期结果
#     with open(test_data_path) as f:
#         test_data = yaml.load(f.read(), Loader=yaml.SafeLoader)
#     tests = test_data['tests']
#     for test_n in tests:
#         case.append(test_n.get('case', ''))
#         http.append(test_n.get('http', {}))
#         expected.append(test_n.get('expected', {}))
#     parameters = zip(case, http, expected)
#     return case, parameters

yaml_data_file = '..\\data\\data_api_login.yaml'
ids, test_datas = get_test_data(yaml_data_file)


def echo_hd5():
    md5 = hashlib.md5()
    md5.update(('2' + '123' + '9d5eb3bdaf6a3c20ae7db90c4161b602211115f1').encode('utf-8'))
    key = md5.hexdigest()
    print(key)


if __name__ == "__main__":
    # print(config_path)
    # print(host)

    # for case, http, expected in test_datas:
    #     host = http['path']
    #     method = http['method']
    #     print(host)
    #     print(method)
    #     headers = http['headers']
    #     print(headers)
    #     data = {
    #         "username": http['params']['username'],
    #         "password": http['params']['password']
    # }
    #     print(data)
    with sqlite3.connect('../db.sqlite3') as conn:
        c = conn.cursor()
        print("Opened database successfully")
        try:
            # cursor = c.execute("SELECT authtoken_token.key,auth_user.username from authtoken_token \
            #                     inner join auth_user on  authtoken_token.user_id=auth_user.id \
            #                     where auth_user.username='caiyingq'")
            cursor = c.execute('SELECT * from api_event where title like "%期%" and type="文娱" and price<=200 and status=0')
            # cursor = c.execute('SELECT * from api_event where title like "%{title}%" and type="{type}" and \
            # price <= {price} and status={status}'.format(title='期', type='文娱', price=200, status=0))

            print(type(cursor))
        except Exception as e:
            print('sss', e)
        else:
            for cu in cursor:
                print(cu)
                for c in cu:
                    print(c, end=' |  ')
                print()
        print(type(conn))

    # print(echo_hd5())
