# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 19:44:09 2022

@author: WWT
"""
from download_fund_info import download_fund_basic_info
from Fund_info import Fund_info
from Fund_strategy import Fund_strategy
from Fund_result_output import Fund_result_output

# if __name__ == '__main__':
"""
下载基金信息
"""
download_fund_basic_info()

"""
基于下载的基金信息进行筛选和过滤，筛选规则见
"""
fund_info = Fund_info()

fund_strategy = Fund_strategy(fund_info)
fund_result_output = Fund_result_output()
fund_strategy.begin_basic_analysis()
fund_strategy.begin_low_valuation_analysis()
for fund_name in fund_strategy.get_low_valuation_fund_names():
    fund_result_output.save_fund_pic(fund_name_code = fund_name, day_nums = 200, dvi = 5)

