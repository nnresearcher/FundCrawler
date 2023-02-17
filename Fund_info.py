# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 11:17:24 2022

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

class Fund_info:
    def __init__(self, csv_names = None, path = 'results/'):
        if csv_names is None:
            self.csv_names = Fund_class.fund_kind_belong_to_index
        else:
            self.csv_names = csv_names
        
        self.csv_path = path
        self.fund_history_struct = Fund_history_struct()
        self.csv_format = '.csv'
        self.all_fund_name = set() # fund_name: 基金名 + '_' + 基金号
        self.all_fund_manager = set()
        self.all_fund_info = dict()
        
        self.load_csv_fund_info() # 去除信息不全的基金 must
        self.del_without_fund_admin_fund() # 删除没有基金经理的基金
        
        
        return;
        
    def merge_fund_info(self, other_fund_info):
        '''
        把两个Fund_info合并
        '''
        for fund_name in other_fund_info.all_fund_name:
            self.all_fund_name.add(fund_name)
        for fund_manager in other_fund_info.all_fund_manager:
            self.all_fund_manager.add(fund_manager)
        self.all_fund_info.update(other_fund_info.all_fund_info)
        return;
        


    def output_fund_picss(self, fund_name_code : str, days = 100, dvi = 1) -> dict:
        """
        输入基金名字输出这个基金的净值曲线图
        fund_name_code:基金名 + '_' + code
        """
        fund_name = fund_name_code[:fund_name_code.index('_')]
        fund_code = fund_name_code[fund_name_code.index('_') + 1:]
        
        '''
        获取该基金的历史信息
        '''
        fund_history = Fund_history_info(fund_code, fund_name)
        self.fund_history_struct = fund_history.get_fund_val_info(days)
        
        '''
        画图
        '''
        if (len(self.fund_history_struct.fund_history_val) < days):
            days = int(len(self.fund_history_struct.fund_history_val)/dvi) * dvi
        x_axis_data = list(sorted(self.fund_history_struct.fund_history_day, reverse=False)[:days])

        y_axis_data = []
        y_axis_data_dvi = []
        for x_data in x_axis_data:
            y_axis_data.append(float(self.fund_history_struct.fund_history_val[x_data]["单位净值"]))
        # plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
        index = 0
        counter = 0
        sums  = 0
        while index < days:
            sums = sums + y_axis_data[index]
            index = index + 1
            counter = counter + 1
            if (counter == dvi):
                y_axis_data_dvi.append(sums/dvi)
                sums = 0
                counter = 0
        label = x_axis_data[::dvi][0] + " to " + x_axis_data[::dvi][-1] + " " + fund_name_code
        plt.plot(x_axis_data[::dvi], y_axis_data_dvi, 'ro-', color='#4169E1', alpha=0.8, linewidth=1, label = label)
        plt.xticks(())
        plt.savefig("pic/" + fund_name_code + ".png")
        plt.close('all')
        
        return;

    """
    加载csv文件地信息，并删除信息不详细的基金信息
    """
    def load_csv_fund_info(self):
        for csv_name in self.csv_names:
            csv_file_name = self.csv_path + csv_name + self.csv_format #
            if os.path.exists(csv_file_name):
                with open (csv_file_name,"r",newline='', encoding='utf-8') as csvfile:
                    readers = csv.reader(csvfile)
                    next(readers) # 删除表头
                    
                    for reader in readers:
                        fund_dic = {}
                        header_counter = 0
                        fund_name = reader[0]
                        fund_code = reader[1]
                        self.all_fund_name.add(fund_name + '_' + fund_code)
                        while (len(reader) != len(Fund_class.write_format_of_index)):
                            reader.append('???')
                        for header in Fund_class.write_format_of_index:
                            fund_dic[header] = reader[header_counter]
                            header_counter = header_counter + 1
                        fund_dic["基金类型"] = csv_name
                        self.all_fund_info[fund_name + '_' + fund_code] = fund_dic
            else:
                print(csv_file_name + "文件不存在")
        return;
    
    
    def del_without_fund_admin_fund(self):
        all_fund_name = copy.deepcopy(self.all_fund_name)
        for fund_name in all_fund_name:
            # 删除找不到基金经理的基金
            if self.all_fund_info[fund_name]["基金经理"] == "???":
                self.all_fund_info.pop(fund_name)
                self.all_fund_name.remove(fund_name)
        return;
        

    # def update_all_fund_manager(self) -> set():
    #     '''
    #     更新这个对象中所有的基金经理列表，并返回
    #     '''
    #     for fund_name in self.all_fund_name:
    #         fund_manager = self.all_fund_info[fund_name]["基金经理"]
    #         if fund_manager == "???" or fund_manager == "":
    #             continue
    #         elif "/" in fund_manager:
    #            while("/" in fund_manager):
    #                self.all_fund_manager.add(fund_manager[ : fund_manager.index("/" )])
    #                fund_manager = fund_manager[fund_manager.index("/" ) + 1 : ]
    #            self.all_fund_manager.add(fund_manager)
    #         else:
    #             self.all_fund_manager.add(fund_manager)
    #     return self.all_fund_manager

    # def get_fund_manager_fund(self, fund_manager : str) -> dict:
    #     """
    #     输入基金经理的名字返回这个基金经理管理的所有基金
    #     """
    #     fund_dic = dict()
    #     fund_manager_fund_name = set()
    #     fund_dic["基金经理"] = fund_manager
    #     for fund_name in self.all_fund_name:
    #         if fund_manager in self.all_fund_info[fund_name]["基金经理"]:
    #             fund_manager_fund_name.add(fund_name)
    #             fund_dic[fund_name] = self.all_fund_info[fund_name]
    #     fund_dic["所有基金名"] = fund_manager_fund_name
    #     return fund_dic
        
        
        
        
        