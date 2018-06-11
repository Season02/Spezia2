# from .baseProducer import base_producer
from ..queue.targetQueue import target_queue

import random
import time

from CoTec.core.SMTP.smtp_go import SMTPServer
from CoTec.core.database.StructureGuard import StructureGuard
from CoTec.core.log.log_go import LogGo
from CoTec.core.request.proxy_go import ProxyHelper
from CoTec.utility.date.date_go import DateGo

from ..etc.somebody_help import somebody_help

from ..dao import scraping_target_dao as ScrabingTarget
from ..dao.soap_target_dao import SoapTargetDao
from ..dao.special_target_dao import SpecialTargetDao
from ..dao.program_dao import ProgramDao
from ..dao.article_dao import ArticleDao

from ..dao.DBStructure import *

from ...scan.dao.scraping_target_dao import get_target_list
from ...scan.dao.scraping_target_dao import reset_target_valid

from ...scan.strategy.web_type import WebStrategy
from ...scan.strategy.wechat_type import WechatStrategy
from ...scan.strategy.weibo_type import WeiboStrategy
from ...scan.strategy.WS3Strategy import WS3Strategy

from ...config.global_var import Configs

from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

import threading

# def target_pool_func_wrapper(instance, i):
#     return instance.worker(i)

target_mutex = threading.Lock()
target_count = 0
target_transported_count = 0
all_target_transported = False

class target_producer(object):
    target_queue = target_queue()

    """
    处理 target 对象，得到 新闻详情页 list 放入 queue
    """

    def __init__(self, targets:list, pool_size, queue_size):
        self.targets = targets

        global target_count, target_transported_count, all_target_transported

        target_count = len(targets)
        target_transported_count = 0
        all_target_transported = False

        # self.target_queue = target_queue(queue_size)
        self.target_queue = target_producer.target_queue

        self.pool_size = pool_size
        self.pool = Pool(processes=pool_size, maxtasksperchild=1)

    # def start(self):
    #     """
    #     开启线程池，把所有 Target 放入池中，单独获取抓取列表
    #     :return:
    #     """
    #     LogGo.info("Start target pool")
    #
    #     while True:
    #         for target in self.targets:
    #             self.worker(target)
    #
    #         time.sleep(8200)

    def start(self):
        """
        开启线程池，把所有 Target 放入池中，单独获取抓取列表
        :return:
        """

        while True:
            LogGo.info("Start target pool")
            [self.pool.apply_async(target_producer.worker, (target,)) for target in self.targets]
            time.sleep(Configs().work_interval)

    @staticmethod
    def send_to_queue(result):
        """
        传送
        code: 0 到达最大访问频率
              1 正常结果
        :param request:
        :param result:
        :return:
        """
        global target_mutex, target_count, target_transported_count, all_target_transported

        code, value = result
        target, detail_page_bundle_list, content_ruler, encode = value

        if code == 1:
            for detail_page_bundle in detail_page_bundle_list:
                target_producer.target_queue.queue.put((target, detail_page_bundle, content_ruler, encode))
                ScrabingTarget.set_last_access_date(target.id)
        else:
            LogGo.error("List Page Error:" + str(target.data_key) + " Code: " + str(code))
            ScrabingTarget.set_elog(target.id, "error code: " + str(code))

        if target_mutex.acquire():
            if target_count == target_transported_count:
                all_target_transported = True
            else:
                target_transported_count += 1
                LogGo.debug('target_transported_count: ' + str(target_transported_count))

            target_mutex.release()

    @staticmethod
    def is_all_target_transported() -> bool:
        global all_target_transported

        return all_target_transported

    # @staticmethod
    # def worker(target):
    @staticmethod
    def worker(target):
        """
        普通扫描函数 首先获取列表 然后抓取详细页内容
        """
        # if not Configs.debuging:
        #     time.sleep(20)
        # time.sleep(1)

        time.sleep(random.randint(1,4))

        last_access = target.last_access_date
        frequency = target.frequency

        if frequency is None:
            frequency = 0
        if last_access is None:
            last_access = DateGo.date_befor_days(365, True)

        distance = DateGo.distance(last_access)

        if distance < frequency:
            ScrabingTarget.set_elog(target.id, "frequency")
            LogGo.info("type: " + str(target.type) + str(target.soap_type) + " name: " + str(target.data_key) + " skipped, last access data: " + str(last_access) + "\r\n")

        if target.type == 'ulweb' or target.type == 'jsweb':
            msg = '>>> Ulweb(' + target.data_key + ')' + ' last acc: ' + str(last_access)
            LogGo.info(msg)

            web = WebStrategy()
            result = web.scrape_list(target)

            target_producer.send_to_queue(result)

        # elif target.type == 'wechat':#微信官方 规律 历史消息
        #     msg = '\r\n' + '>>> Wechat(' + target.extra0 + ')'
        #     LogGo.info(msg)
        #     wechat = WechatStrategy()
        #     result = wechat.ScanWechatTarget(target)
        #
        #     return (target, 1, result)

        elif target.type == 'newrank':
            msg = '>>> Newrank(' + target.extra0 + ')' + ' last acc: ' + str(last_access)
            LogGo.info(msg)

            wechat = WechatStrategy()
            result = wechat.newrank_list(target)

            target_producer.send_to_queue(result)

        elif target.type == 'gsdata':
            msg = '>>> Gsdata(' + target.extra0 + ')' + ' last acc: ' + str(last_access)
            LogGo.info(msg)

            wechat = WechatStrategy()
            result = wechat.gs_list(target)

            target_producer.send_to_queue(result)

        elif target.type == 'weibo':
            msg = '>>> Weibo(' + target.extra0 + ')' + ' last acc: ' + str(last_access)
            LogGo.info(msg)

            weibo = WeiboStrategy()
            result = weibo.weibo_list(target)

            target_producer.send_to_queue(result)
