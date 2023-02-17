# -*- coding:UTF-8 -*-
"""
负责接受url并爬取该网页
"""
import threading
from abc import ABC
from multiprocessing import Process, Queue, Event
from time import time

from download_fund_info.FakeUAGetter import my_fake_ua


class GetPage:
    """
    获取页面基类，从_task_queue中获取任务，输出结果到_result_queue中
    """

    def __init__(self):
        self._task_queue = None
        self._result_queue = None


class GetPageByWeb(GetPage, ABC):
    """
    从网页中获取页面基类
    """

    @classmethod
    def get_page_context(cls, url, timeout, *args) -> tuple:
        """
        用于爬取页面 爬取特定的网页
        :param timeout: 爬取timeout设置，可为一个数字，或一个元组
        :param url:要爬取的url
        :return: 返回二元组 爬取结果，网页内容
        """
        header = {"User-Agent": my_fake_ua.random}
        import requests
        try:
            page = requests.get(url, headers=header, timeout=timeout)
            page.encoding = 'utf-8'
            # fixme 临时措施 返回内容为空视为错误
            # 反爬虫策略之 给你返回空白的 200结果
            if page.text:
                result = ('success', page.text, *args)
            else:
                result = ('error', url, *args)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
            result = ('error', url, *args)
        return result


class GetPageByWebWithAnotherProcessAndMultiThreading(Process, GetPageByWeb):
    """
    启动另一个进程，并在这个进程中使用多线程来爬取网页
    将爬取任务发送到 task_queue，并在完成后将 exit_sign 设置为True
    进程会在所有的任务都完成后，将 exit_sign 设置为False，并在result_queue中的item取完后退出
    """
    # 描述在持续几秒连接失败之后向用户展示提示信息，单位 秒
    SHOW_NETWORK_DOWN_LIMIT_TIME = 3

    def __init__(self, task_queue: Queue, result_queue: Queue, exit_sign: Event, network_health: Event):
        super().__init__()
        self._task_queue = task_queue
        self._result_queue = result_queue
        self._threading_pool = list()
        self._exit_when_task_queue_empty = exit_sign
        self._max_threading_number = 2
        self._record_network_down_last_time = None
        self._network_health = network_health
        self._timeout = 3

    def add_task(self, task):
        self._task_queue.put(task)

    def get_result(self) -> Queue:
        return self._result_queue

    def get_page_context_and_return_in_queue(self, url, *args):
        print("xxxxxxxxxx")
        result = super().get_page_context(url, self._timeout, *args)      
        if result[0] == 'success':
            # 成功了，进程再增加看看
            self._max_threading_number += 1
            if self._network_health.is_set():
                self._record_network_down_last_time = None
                self._network_health.clear()
        else:
            # 失败了降低一下进程数量看看
            if self._max_threading_number > 1 :
                self._max_threading_number = self._max_threading_number >> 1
            else:
                self._max_threading_number = 1
            
            # 如果最大进程数已经降低到最小，并且_network_health没有被置起（说明之前认为网络没问题）
            # 检查下是不是连续3秒没有成功过，如果是那么就认为网络有问题了，置起网络健康事件
            if self._max_threading_number == 1 and not self._network_health.is_set():
                if self._record_network_down_last_time is None:
                    self._record_network_down_last_time = time()
                elif time() - self._record_network_down_last_time > \
                        GetPageByWebWithAnotherProcessAndMultiThreading.SHOW_NETWORK_DOWN_LIMIT_TIME:
                    self._network_health.set()
                    self._record_network_down_last_time = time()
        self._result_queue.put(result)

    def run(self) -> None:
        while True:
            
            if self._task_queue.empty() and len(self._threading_pool) == 0: 
                if self._exit_when_task_queue_empty.is_set():
                    self._exit_when_task_queue_empty.clear()
                    break
                else:
                    continue
            else:
                # 1 清除死去的线程
                # 2 新建新的线程
                for t in self._threading_pool:
                    if not t.is_alive():
                        self._threading_pool.remove(t)

                while self._task_queue.qsize() > 0 and len(self._threading_pool) < self._max_threading_number:
                    # 那么就从进程中获取一个任务
                    task = self._task_queue.get()
                    t = threading.Thread(target=self.get_page_context_and_return_in_queue,
                                         args=(task[0], *task[1:]))
                    self._threading_pool.append(t)
                    t.start()
