# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 19:41:42 2022

@author: WWT
"""

import os
import time
import traceback
import sys
if 'darwin' in sys.platform:
    from methods import Queue
else:
    from multiprocessing import Queue

from download_fund_info.FundListProvider import GetFundListFromWeb, GetFundListTest
from download_fund_info.crawling_fund import crawling_fund
def download_fund_basic_info():

    # 记录开始时间
    start_time = time.time()

    # 干活
    try:
        # 获取当前网络上的基金列表
        fund_list = GetFundListFromWeb()

        # 在这里更换提供基金列表的类，以实现从文件或者其他方式来指定要爬取的基金
        fail_list = crawling_fund(fund_list)
        print(fail_list)
    except Exception:
        print('不知道为了什么，程序死掉了。')
        traceback.print_exc()

    # 输出总时间
    print(f'\n爬取基金基础信息总用时{time.time() - start_time} s')