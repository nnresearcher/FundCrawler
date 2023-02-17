# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 11:37:52 2022

@author: WWT
"""

class Fund_class:
    """
    指数型基金
    """
    # 指数型基金
    fund_kind_belong_to_index = ['股票型', '混合型-偏股', '混合型-灵活', '混合型-平衡',
     '混合型-偏债', '指数型-股票','债券型-长债',
     '债券型-混合债', '债券型-可转债', '债券型-中短债',
     'QDII', '商品（不含QDII）', '混合-绝对收益', 'FOF']
    # 指数型基金的解析定义
    parse_index_for_index_fund = ['近1月', '近1年', '近3月', '近3年', '近6月', '成立来']
    
    # 指数型基金的表格内容
    write_format_of_index = ['基金名称', '基金代码', '基金规模', '近1月', '近3月',
     '近6月', '近1年', '近3年', '成立来', '基金经理',
     '任职时间', '任期收益', '总任职时间']
    
    """
    保本型基金
    """
    # 保本型基金
    fund_kind_belong_to_guaranteed = ['保本型']

    # 保本型基金的表格内容
    write_format_of_guaranteed = ['基金名称', '基金代码', '基金规模', '保本期收益', '近1月',
     '近3月', '近6月', '近1年', '近3年', '基金经理', '任职时间',
     '任期收益', '总任职时间']
    
    # 保本型基金的解析定义
    parse_index_for_guaranteed_fund = ['保本期收益', '近6月', '近1月', '近1年', '近3月', '近3年']
    
    """
    固定收益型基金
    """
    # 固定收益型基金
    fund_kind_belong_to_closed_period = ['固定收益']
    
    # 固定收益型基金的表格内容
    write_format_of_capital_preservation = ['基金名称', '基金代码', '基金规模', '最近约定年化收益率',
     '基金经理', '任职时间', '任期收益', '总任职时间']

    # 固定收益型的解析定义
    parse_index_for_capital_preservation_fund = ['最近约定年化收益率']
    def __init__(self):
        return

        