#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019-
@Author: GaoKang
Project description：
"""

import os
import time


def main():
    """
    主函数
    """
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'api_cases')
    cmd = "pytest -s -v {} --env=super".format(path)
    print(cmd)
    result = os.popen(cmd)
    time.sleep(1)
    while True:
        result_echo = result.read()
        if result_echo:
            print(result_echo)
        else:
            break


if __name__ == "__main__":
    main()
