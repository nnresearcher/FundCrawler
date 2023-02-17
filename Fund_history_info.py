# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 15:13:26 2022

https://zhuanlan.zhihu.com/p/141727806

@author: WWT
"""
from download_fund_info.FakeUAGetter import my_fake_ua
import requests
import time

from Fund_history_struct import Fund_history_struct
class Fund_history_info():
    def __init__(self, fund_code, fund_name):
        self.fund_code = fund_code
        self.fund_name = fund_name
        self.fund_history_struct = Fund_history_struct()
        
    def get_fund_val_info(self, days : int) -> Fund_history_struct:
        url = self.get_fund_vale_url(1)
        fund_text = self.get_url_text(url)
        fund_basic_info = self.get_url_basic_info(url, fund_text)
        
        if (int(fund_basic_info["records"]) < days):
            print(self.fund_name + "成立的日期不足" + str(days) + "天, 仅有" + fund_basic_info["records"] + "天。")
            nee_day_num = int(fund_basic_info["records"])
        else:
            nee_day_num = days
        
        pages = 0
        while(self.fund_history_struct.fund_history_day_num < nee_day_num):
            pages = pages + 1
            url = self.get_fund_vale_url(pages)
            fund_text = self.get_url_text(url)
            self.update_history_value_info(url, fund_text)
        return self.fund_history_struct

    def get_url_text(self, url):
        """
        计算每日基金净值的链接
        url  :要解析的网址
        """
        header = {"User-Agent": my_fake_ua.random}
        pages = requests.get(url, headers=header, timeout=3)
        pages.encoding = 'utf-8'
        return pages.text    
    def update_history_value_info(self, url, url_text=None):
        """
        计算每日基金净值的链接
        url  :要解析的网址
        return :返回值为字典，
                键值：tile表示这个网址里面表格的表头
                     info表示这个表格的内部信息
        """
        title = ["净值日期","单位净值", "累计净值", 
             "日增长率","申购状态", "赎回状态", 
             "分红送配"]
        divide_info = []
        detail_infos = []
        
        if url_text is None:
            url_text = self.get_url_text(url)
            
        '''
        解析网址
        var apidata={ content:"
        净值日期	单位净值	累计净值	日增长率	申购状态	赎回状态	分红送配
        2002-01-18	1.0000	1.0000	-0.10%	封闭期	封闭期	
        2002-01-11	1.0010	1.0010	0.10%	封闭期	封闭期	
        2002-01-04	1.0000	1.0000	0.00%	封闭期	封闭期	
        2001-12-28	1.0000	1.0000	0.00%	封闭期	封闭期	
        2001-12-21	1.0000	1.0000	0.00%	封闭期	封闭期	
        2001-12-18	1.0000	1.0000		封闭期	封闭期	
        ",records:4466,pages:224,curpage:224};
        '''
        '''
        解析完成后，detail_infos数据样式

        2002-01-18	1.0000	1.0000	-0.10%	封闭期	封闭期	
        2002-01-11	1.0010	1.0010	0.10%	封闭期	封闭期	
        2002-01-04	1.0000	1.0000	0.00%	封闭期	封闭期	
        2001-12-28	1.0000	1.0000	0.00%	封闭期	封闭期	
        2001-12-21	1.0000	1.0000	0.00%	封闭期	封闭期	
        2001-12-18	1.0000	1.0000	    	封闭期	封闭期	
        '''
        url_text = url_text[url_text.index('<tr><td>'):]
    
        while ('<tr><td>' in url_text):
            divide_info.append(url_text[:url_text.index('</td></tr>') + 10])
            url_text = url_text[url_text.index('</td></tr>') + 10:]
        
        for info in divide_info:
            tmp = []
            info = info[4:]
            while("</td>" in info):
                tmp.append(info[info.index(">") + 1:info.index("</td>")])
                info = info[info.index("</td>")+5:]
            detail_infos.append(tmp)
        
        '''
        开始储存数据
        '''
        for detail_info in detail_infos:
            self.fund_history_struct.fund_history_day.add(detail_info[0])
            
            fund_per_day_info = dict()
            for i in range(1, len(title)):
                fund_per_day_info[title[i]] = detail_info[i]
            self.fund_history_struct.fund_history_val[detail_info[0]] = fund_per_day_info
        
        self.fund_history_struct.title = set(title)
        self.fund_history_struct.fund_history_day_num = len(self.fund_history_struct.fund_history_day)
    
    def get_fund_vale_url(self, page = 1, per = 49,  sdate = "2000-01-01", edate = None) -> str:
        """
        计算每日基金净值的链接
        code  :基金代码
        sdate :数据开始日期等于2001-12-18
        edate :数据结束日期等于2020-05-18
        per   :每页显示的条数，最大为50
        page  :一页显示不完整，该参数直接指定显示第几页
        """
        if edate == None:
            edate = time.strftime("%Y-%m-%d", time.localtime())
        base_url  = "https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz"
        code_url  = "&code="  + self.fund_code
        sdate_url = "&sdate=" + sdate
        edate_url = "&edate=" + edate
        per_url   = "&per="   + str(per)
        page_url  = "&page=" + str(page)
        url = base_url + code_url + sdate_url + edate_url + per_url + page_url
        return url
    

    
    
    def get_url_basic_info(self, url, url_text=None) -> dict:
        """
        计算每日基金净值的链接
        url  :要解析的网址
        return :返回值为字典，
                键值：pages表示一共有多少页
                     records表示一共有多少项
                     curpage表示当前在第几页
        """
        if url_text is None:
            url_text = self.get_url_text(url)
        if ("pages" not in url_text):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("url:" + url)
            print("url_text:" + url_text)
        pages = url_text[url_text.index("pages:") + 6 : url_text.index(",curpage")]
        records = url_text[url_text.index("records:") + 8 : url_text.index(",pages")]
        curpage = url_text[url_text.index("curpage:") + 8 : url_text.index("};")]
        url_dic = {}
        url_dic["pages"] = pages
        url_dic["records"] = records
        url_dic["curpage"] = curpage
        return url_dic
    
    
    
    
    
    
    