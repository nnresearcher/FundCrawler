# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 21:04:36 2022

@author: WWT
"""
import csv
import os
import copy
from Fund_info import Fund_info
from Fund_class import Fund_class
def read_basic_info_csv(csv_file : str, headers : list, fund_type : list) -> Fund_info:
    csv_info = Fund_info()
    all_fund_name = []
    
    if os.path.exists(csv_file):
        with open (csv_file,"r",newline='') as csvfile:
            readers = csv.reader(csvfile)
            next(readers) # 删除表头
            
            for reader in readers:
                fund_dic = {}
                header_counter = 0
                fund_name = reader[0]
                fund_code = reader[1]
                all_fund_name.append(fund_name + '_' + fund_code)
                while (len(reader) != len(headers)):
                    reader.append('???')
                for header in headers:
                    fund_dic[header] = reader[header_counter]
                    header_counter = header_counter + 1
                fund_dic["基金类型"] = fund_type
                csv_info.all_fund_info[fund_name + '_' + fund_code] = fund_dic
    csv_info.all_fund_name = set(all_fund_name)
    return csv_info


def load_fund_basic_info() -> Fund_info:
    csv_total_info = Fund_info()
    for fund_type in Fund_class.fund_kind_belong_to_index:
        csv_name = "results/" + fund_type + ".csv"
        csv_total_info.merge_fund_info(read_basic_info_csv(csv_name, Fund_class.write_format_of_index, fund_type))
    return csv_total_info


def parser_fund_basic_info(need_parser = True):
    csv_total_info = load_fund_basic_info()
    if need_parser:
        all_fund_name = copy.deepcopy(csv_total_info.all_fund_name)
        for fund_name in all_fund_name:
            # 删除找不到基金经理的基金
            if csv_total_info.all_fund_info[fund_name]["基金经理"] == "???":
                csv_total_info.all_fund_info.pop(fund_name)
                csv_total_info.all_fund_name.remove(fund_name)
                continue
            
            # 删除成立不到一年的基金
            #if (csv_total_info.all_fund_info[fund_name]["近3年"]) == '--':
            #    csv_total_info.all_fund_info.pop(fund_name)
            #    csv_total_info.all_fund_name.remove(fund_name)
            #    continue
            
            
            # 删除负收益差的基金
            if '-' in csv_total_info.all_fund_info[fund_name]["近1月"]:
                csv_total_info.all_fund_info.pop(fund_name)
                csv_total_info.all_fund_name.remove(fund_name)
                continue
            if '-' in csv_total_info.all_fund_info[fund_name]["成立来"]:
                csv_total_info.all_fund_info.pop(fund_name)
                csv_total_info.all_fund_name.remove(fund_name)
                continue
            if '-' in csv_total_info.all_fund_info[fund_name]["近3年"]:
                csv_total_info.all_fund_info.pop(fund_name)
                csv_total_info.all_fund_name.remove(fund_name)
                continue
            
            # 删除收益差的基金
            if float(csv_total_info.all_fund_info[fund_name]["近1月"][:-1]) < 3:
                csv_total_info.all_fund_info.pop(fund_name)
                csv_total_info.all_fund_name.remove(fund_name)
                continue
            if float(csv_total_info.all_fund_info[fund_name]["成立来"][:-1]) < 50:
                csv_total_info.all_fund_info.pop(fund_name)
                csv_total_info.all_fund_name.remove(fund_name)
                continue
    return csv_total_info

