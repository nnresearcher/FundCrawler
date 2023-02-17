# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 14:36:23 2022

@author: WWT
"""

class Attribute_cfg:
    
    # 是否删除从来不赚钱的基金
    need_del_never_make_money_fund = True

    # 是否删除成立时间不超过一年的基金
    need_del_short_establishment_fund = True

    # 是否删除近3个月赚太多的基金
    need_del_three_month_make_money_a_lot_fund = True
    # 近3个月收益阈值，超过这个的会被删除
    three_month_make_month_threshold = 30
    
    # 是否删除近1个月亏损太多的基金
    need_del_one_month_lost_money_a_lot_fund = True
    # 近1个月亏损超过这个阈值的基金会被删除
    one_month_lost_money_threshold = -15
    
    def __init__(self):
        return
