# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 14:31:18 2022

@author: WWT
"""

class Fund_history_struct():
    
    def __init__(self):
        self.fund_history_day = set()
        self.fund_history_day_num = 0
        self.fund_history_val = dict()
        self.title = set()