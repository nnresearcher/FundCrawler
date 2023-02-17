# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 17:56:21 2022

@author: WWT
"""

'''
基金总的信息处理
'''
import csv
import os
import copy
from Fund_history_info import Fund_history_info
from Fund_class import Fund_class

from Fund_history_struct import Fund_history_struct
import matplotlib.pyplot as plt

class Fund_result_output:
    def __init__(self):
        return;


    def save_fund_pic(self, fund_name_code : str, day_nums = 100, dvi = 1):
        """
        输入基金名字输出这个基金的净值曲线图
        fund_name_code:基金名 + '_' + code
        """
        fund_name = self.__get_fund_name(fund_name_code)
        fund_code = self.__get_fund_code(fund_name_code)
        if ('/' in fund_name):
            fund_name = fund_name.replace('/', '_')
        '''
        获取该基金的历史信息
        '''
        self.fund_history_struct = self.__get_fund_history_info(fund_code, fund_name, day_nums)
        day_nums = self.__recalculate_day_nums(day_nums, dvi)
        
        all_dates = self.__get_all_date(day_nums)
        all_history_vals = self.__get_all_history_val(all_dates)
        
        all_dvied_dates = self.__dvi_all_dates(all_dates, dvi)
        all_dvied_history_vals = self.__dvi_all_history_val(all_history_vals, day_nums, dvi)
        
        '''
        画图
        '''
        label = all_dvied_dates[0] + " to " + all_dvied_dates[-1] + " " + fund_name_code
        plt.plot(all_dvied_dates, all_dvied_history_vals, 'ro-', color='#4169E1', alpha=0.8, linewidth=1, label = label)
        plt.xticks(())
        plt.savefig("pic/" + fund_name + "_" + fund_code + ".png")
        plt.close('all')
        return;
        
    def __get_fund_code(self, fund_name_code):
        fund_code = fund_name_code[fund_name_code.index('_') + 1:]
        return fund_code
    
    def __get_fund_name(self, fund_name_code):
        fund_name = fund_name_code[:fund_name_code.index('_')]
        return fund_name
    
    def __get_fund_history_info(self, fund_code, fund_name, day_nums):
        fund_history = Fund_history_info(fund_code, fund_name)
        return fund_history.get_fund_val_info(day_nums)
        
    def __recalculate_day_nums(self, day_nums, dvi):
        if (len(self.fund_history_struct.fund_history_val) < day_nums):
            day_nums = int(len(self.fund_history_struct.fund_history_val) / dvi) * dvi
        return day_nums
        
    def __get_all_date(self, day_nums):
        return list(sorted(self.fund_history_struct.fund_history_day, reverse=False)[:day_nums])
    
    def __get_all_history_val(self, all_dates):
        all_history_vals = []
        for date in all_dates:
            all_history_vals.append(float(self.fund_history_struct.fund_history_val[date]["单位净值"]))
        return all_history_vals
    
    def __dvi_all_dates(self, all_dates, dvi):
        return all_dates[::dvi]
    
    def __dvi_all_history_val(self, all_history_vals, day_nums, dvi):
        dvied_history_val = []
        index = 0
        while index < day_nums:
            sums = 0
            for _ in range(dvi):
                sums = sums + all_history_vals[index]
                index = index + 1
            dvied_history_val.append(sums/dvi)
        return dvied_history_val
            