# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 16:55:40 2022

@author: WWT
"""
import copy
from Fund_info import Fund_info
from Attribute_cfg import Attribute_cfg

class Fund_strategy:
    def __init__(self, Fund_info : Fund_info):
        self.all_fund_info = Fund_info.all_fund_info
        self.all_fund_name = Fund_info.all_fund_name
        
        self.basic_filter = False
        self.basic_filter_fund_info = None
        self.basic_filter_fund_name = None
        
        self.low_valuation_fund_filter = False
        self.low_valuation_fund_info = None
        self.low_valuation_fund_name = None
        
        self.three_month_make_month_threshold = Attribute_cfg.three_month_make_month_threshold
        self.one_month_lost_money_threshold = Attribute_cfg.one_month_lost_money_threshold
        return;
    
    def begin_basic_analysis(self):
        fund_infos = copy.deepcopy(self.all_fund_info)
        fund_names = copy.deepcopy(self.all_fund_name)
       
        if Attribute_cfg.need_del_short_establishment_fund == True:
           fund_infos, fund_names = self.__del_short_establishment_fund(fund_infos, fund_names) # 删除成立时间不足一年的基金
            
        if Attribute_cfg.need_del_never_make_money_fund == True:
            fund_infos, fund_names = self.__del_never_make_money_fund(fund_infos, fund_names) # 删除从不赚钱的基金
            
        if Attribute_cfg.need_del_three_month_make_money_a_lot_fund == True:
            fund_infos, fund_names = self.__del_three_month_make_money_a_lot_fund(fund_infos, fund_names) # 删除近3个月赚太多的基金
        
        if Attribute_cfg.need_del_one_month_lost_money_a_lot_fund == True:
            fund_infos, fund_names = self.__del_one_month_lost_money_a_lot_fund(fund_infos, fund_names) # 删除近1个月亏太多的基金
        self.basic_filter = True
        self.basic_filter_fund_info = fund_infos
        self.basic_filter_fund_name = fund_names
        return
    
    def begin_low_valuation_analysis(self):
        if self.basic_filter == False:
            print("未进行基础数据分析，无法进行低估值基金分析")
        else:
            fund_infos = copy.deepcopy(self.basic_filter_fund_info)
            fund_names = copy.deepcopy(self.basic_filter_fund_name)
            fund_infos, fund_names = self.__search_low_valuation_fund(fund_infos, fund_names)
            self.low_valuation_fund_filter = True
            self.low_valuation_fund_info = fund_infos
            self.low_valuation_fund_name = fund_names
        return
    
    def get_low_valuation_fund_names(self):
        if self.low_valuation_fund_filter == False:
            print("未进行低估值基金分析!!!!，无法获取有效地低估值基金信息")
        return self.low_valuation_fund_name
        
    def __del_short_establishment_fund(self, fund_infos, fund_names):
        all_fund_name = copy.deepcopy(fund_names)
        for fund_name in all_fund_name:
            if '--' in fund_infos[fund_name]["近1年"]:
                fund_infos.pop(fund_name)
                fund_names.remove(fund_name)
        return fund_infos, fund_names;

    def __del_never_make_money_fund(self, fund_infos, fund_names):
        all_fund_name = copy.deepcopy(fund_names)
        for fund_name in all_fund_name:

            # 删除成立不足1年的基金
            if '-' in fund_infos[fund_name]["成立来"]:
                fund_infos.pop(fund_name)
                fund_names.remove(fund_name)
        return fund_infos, fund_names;

    def __del_three_month_make_money_a_lot_fund(self, fund_infos, fund_names):
        threshold = self.three_month_make_month_threshold
        all_fund_name = copy.deepcopy(fund_names)
        for fund_name in all_fund_name:
            if float(fund_infos[fund_name]["近3月"][:-1]) > threshold:
                fund_infos.pop(fund_name)
                fund_names.remove(fund_name)
        return fund_infos, fund_names;
    
    def __del_one_month_lost_money_a_lot_fund(self, fund_infos, fund_names):
        threshold = self.one_month_lost_money_threshold
        all_fund_name = copy.deepcopy(fund_names)
        for fund_name in all_fund_name:
            if float(fund_infos[fund_name]["近1月"][:-1]) < threshold:
                fund_infos.pop(fund_name)
                fund_names.remove(fund_name)
        return fund_infos, fund_names;
        
        
    def __search_low_valuation_fund(self, fund_infos, fund_names):
        all_fund_name = copy.deepcopy(fund_names)
        for fund_name in all_fund_name:
            if not ((float(fund_infos[fund_name]["近1月"][:-1]) < 5) and
                    (float(fund_infos[fund_name]["近1月"][:-1]) > 0) and
                    (float(fund_infos[fund_name]["近3月"][:-1]) > -20) and
                    (float(fund_infos[fund_name]["近3月"][:-1]) < -10)
                    ):
                fund_infos.pop(fund_name)
                fund_names.remove(fund_name)
        return fund_infos, fund_names;
        