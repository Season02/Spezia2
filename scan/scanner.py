from CoTec.core.SMTP.smtp_go import SMTPServer
from CoTec.core.database.StructureGuard import StructureGuard
from CoTec.core.log.log_go import LogGo
from CoTec.core.request.proxy_go import ProxyHelper

from .etc.somebody_help import somebody_help

from .dao.soap_target_dao import SoapTargetDao
from .dao.special_target_dao import SpecialTargetDao
from .dao.program_dao import ProgramDao
from .dao.article_dao import ArticleDao

from .dao.DBStructure import *

from ..scan.dao.scraping_target_dao import get_target_list
from ..scan.strategy.WS3Strategy import WS3Strategy

import time

from ..config.global_var import Configs

from .producer.targetProducer import target_producer
from .consumer.targetConsumer import target_consumer
from .consumer.uploadConsumer import upload_consumer

from .queue.targetQueue import target_queue
from .queue.uploadQueue import upload_queue

from CoTec.core.request.proxy_go import ProxyHelper
from CoTec.core.database.mysql_go import MysqlHelper

from CoTec.core.request.request_class_ver import RequestHelperClassVer

class Scanner:

    def __init__(self):
        self.special = SpecialTargetDao()
        self.exist_program = ProgramDao().get_all_title_cn()
        # self.exist_news = NewsDao().get_all_title()
        self.exists_weibo_ids =  ArticleDao().get_all_identifier()

        self.config = Configs()

    @ProxyHelper.where_i_am
    def start(self):
        try:
            if self.config.check_table:
                self.check_data_base()

            # RequestHelperClassVer.init(self.config)
            # ProxyHelper.init(self.config)
            # MysqlHelper.init(self.config)

            self.start_mormal_mission()
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

    def start_mormal_mission(self):
        global all_target_transported

        target_list = get_target_list()

        self.target_producer = target_producer(target_list, self.config.target_pool_size, self.config.target_queue_size)
        self.target_consumer = target_consumer()
        self.upload_consumer = upload_consumer(self.config.uploader_queue_size)

        self.upload_consumer.start()
        self.target_consumer.start()
        self.target_producer.start()

        # self.target_producer.pool.close()
        # self.target_producer.pool.join()

        while True:            # LogGo.debug(">>> target queue unfinishd count: " + str(self.target_producer.target_queue.queue.unfinished_tasks))
            time.sleep(5)
            LogGo.debug("target_transported_over: " + str(target_producer.is_all_target_transported()))

        # self.target_consumer.queue.queue.join()
        # time.sleep(6000)

        LogGo.info('Loop Done! task count: ' + str(len(target_list)))
        SMTPServer.launch_mission_report()

    def update_index(self):
        # somebody_help.update_index()
        pass

    def check_data_base(self):
        """数据库结构检查"""

        list = [TBNews(), TBArticle(), TBProgram(), TBWenzhangInfo(), TBDictionaryType(), TBDictionary(), TBNewsGroup(), TBNlpFilter(), TBScrapingTarget(), TBSoap(), TBSoapTarget(), TBGlobalTarget(), TBMR(), TBSpecialTarget(), TBProgramType(), TBSoapBlackList(), TBHeavyText()]
        # list = [TBSoapBlackList()]

        guard = StructureGuard(Configs())
        log = guard.check(list)

        if len(log) > 0:
            LogGo.info(str(log))


