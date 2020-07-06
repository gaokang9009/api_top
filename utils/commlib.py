#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：Util of project
"""

import configparser
import yaml
import sqlite3
import hashlib


class ApiConfig(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.file_list = self.config.read(file_path)

    def get_config_data(self, section, key):
        get_data = None
        if not self.file_list:
            print('"{}" is not exists.'.format(self.file_path))
        else:
            try:
                get_data = self.config.get(section, key)
            except Exception as e:
                print('"{}" file do not have the config which section is "{}" key is "{}", '
                      .format(self.file_path, section, key), e)
        return get_data

    def add_config_data(self, section, key, value):
        if section not in self.config.sections():
            self.config.add_section(section)
        try:
            self.config.set(section, key, value)
        except Exception as e:
            print('"{}" file add config failed, which section is "{}" key is "{}" value is {}, '
                  .format(self.file_path, section, key, value), e)
            return False
        else:
            with open(self.file_path, 'w') as f:
                self.config.write(f)
            return True


def get_config_data1(file_path, section, key):
    config = configparser.ConfigParser()
    file_list = config.read(file_path)
    get_data = None
    if not file_list:
        print('"{}" is not exists.'.format(file_path))
    else:
        try:
            get_data = config.get(section, key)
        except Exception as e:
            print('"{}" file do not have the config which section is "{}" key is "{}", '
                  .format(file_path, section, key), e)
    return get_data


def add_config_data1(file_path, section, key, value):
    config = configparser.ConfigParser()
    config.read(file_path)
    if section not in config.sections():
        config.add_section(section)
    try:
        config.set(section, key, value)
    except Exception as e:
        print('"{}" file add config failed, which section is "{}" key is "{}" value is {}, '
              .format(file_path, section, key, value), e)
    else:
        with open(file_path, 'w') as f:
            config.write(f)
        return True


def get_test_data(test_data_path):
    case = []  # 测试用例名称
    http = []  # 请求对象
    expected = []  # 预期结果
    with open(test_data_path, 'r', encoding='UTF-8') as f:
        test_data = yaml.load(f.read(), Loader=yaml.SafeLoader)
    tests = test_data['tests']
    for test_n in tests:
        case.append(test_n.get('case', ''))
        http.append(test_n.get('http', {}))
        expected.append(test_n.get('expected', {}))
    parameters = zip(case, http, expected)
    return case, parameters


def get_data_from_database(database, sql):
    with sqlite3.connect(database) as conn:
        c = conn.cursor()
    # print("Opened database successfully")
    try:
        cursor = c.execute(sql)
    except Exception as e:
        print(e)
    else:
        return cursor


def echo_hd5(uid, rstr, token):
    md5 = hashlib.md5()
    md5.update((str(uid)+str(rstr)+str(token)).encode('utf-8'))
    key = md5.hexdigest()
    return key


if __name__ == "__main__":
    path = 'E:\\api_top\\config\\config_normal\\config.ini'
    my_config = ApiConfig(path)
    my_config.get_config_data('login', 'username')
    my_config.get_config_data('login', 'username1')
    my_config.add_config_data('login2', 'username2', 'dasdadasf121')
    my_config.add_config_data('sessions', 'session', 'mysession')