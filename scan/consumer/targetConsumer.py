import threading
import time
import random

from .baseConsumer import base_consumer
from ..queue.targetQueue import target_queue
from ..queue.uploadQueue import upload_queue

from ...scan.strategy.web_type import WebStrategy
from ...scan.strategy.wechat_type import WechatStrategy
from ...scan.strategy.weibo_type import WeiboStrategy

from CoTec.core.log.log_go import LogGo

class target_consumer(threading.Thread):
    """
    读取 target 队列 处理 target 得到待抓取的 详细页 列表（包含地址，标题等信息）
    然后发送至 upload queue 处理
    """
    def __init__(self):
        super().__init__()
        self.target_queue = target_queue()
        self.upload_queue = upload_queue()
        self.base = base_consumer()

        self.web = WebStrategy()
        self.wechat = WechatStrategy()
        self.weibo = WeiboStrategy()

    def run(self):
        while True:
            value = self.target_queue.queue.get()  # 当队列为空时，会阻塞，直到有数据
            self.base.get_thread(self.fetch_detail, value)
            self.target_queue.queue.task_done()
            time.sleep(random.randint(1, 5))
            # time.sleep(5)

    def fetch_detail(self, value):
        """value: (target, original dic, ruler, encode  )
        """
        LogGo.debug("in detail :" + str(value))
        target, detail_page_dic, content_ruler, encode = value

        delegate = None

        if target.type == 'ulweb' or target.type == 'jsweb':
            delegate = self.web.scrape_detail
        elif target.type == 'newrank':
            delegate = self.wechat.newrank_detail
        elif target.type == 'gsdata':
            delegate = self.wechat.gs_detail
        elif target.type == 'weibo':
            delegate = self.weibo.weibo_detail

        code, result_dic = delegate(target, detail_page_dic, content_ruler, encode)

        if code is 1:
            self.upload_queue.queue.put(result_dic)
        else:
            LogGo.error("Detail Error: " + str(detail_page_dic))
