#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020
@Author: GaoKang
Project description：
"""

import os
import time


def excute_cmd_echo_out(cmd_list):
    for cmd in cmd_list:
        print(cmd)
        with os.popen(cmd) as  result:
            while True:
                result_echo = result.read()
                if result_echo:
                    print(result_echo)
                    time.sleep(0.1)
                else:
                    break


def main():
    """
    主函数
    """
    root_path = os.path.split(os.path.realpath(__file__))[0]
    case_path = os.path.join(root_path, 'api_cases')
    allure_results_path = os.path.join(root_path, 'allure_results', 'results_'+time.strftime('%Y%m%d%H%M%S'))
    allure_reports_path = os.path.join(root_path, 'allure_reports', 'reports_'+time.strftime('%Y%m%d%H%M%S'))
    cmd_list = ['pytest {} --alluredir {}'.format(case_path, allure_results_path),
                'allure generate {} -o {}'.format(allure_results_path, allure_reports_path)]
    # 'allure open {}'.format(allure_reports_path)
    excute_cmd_echo_out(cmd_list)


if __name__ == "__main__":
    main()
