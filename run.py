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
    path = os.path.join(os.getcwd(), 'api_cases')
    cmd = "pytest -s -v {} --env=super".format(path)
    print(cmd)
    result = os.popen(cmd)
    # time.sleep(5)
    # print(result.read())


if __name__ == "__main__":
    main()
