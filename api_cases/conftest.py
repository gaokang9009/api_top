#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：
pytest conftest
"""
import os
import pytest
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


@pytest.fixture(scope='session')
def get_sessionid():
    pass

