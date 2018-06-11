from ...scan.dao.article_dao import ArticleDao
from ...scan.dao.news_dao import NewsDao
from ...scan.dao.soap_dao import SoapDao
from ...scan.dao.play_count_dao import PlayCountDao
from ...scan.dao.program_dao import ProgramDao
from ...scan.dao.program_type_dao import ProgramTypeDao
from ...scan.dao.soap_target_dao import SoapTargetDao
from ...scan.dao.black_soap_dao import BlackSoapDao
from ...scan.dao.heavy_text_dao import HeavyTextDao
from ...scan.dao.DBStructure import *

from CoTec.utility.string.string_go import genUUID
from CoTec.core.log.log_go import LogGo

# import threading

# mutex = threading.Lock()
class BaseStrategy(object):
    web_order = None
    wechat_order = None
    weibo_order = None
    exists_url = None
    exists_title = None
    exists_signature = None
    exists_identifier = None

    def __init__(self):
        self.news = NewsDao()
        self.article = ArticleDao()
        self.soap = SoapDao()
        self.pc = PlayCountDao()
        self.program = ProgramDao()
        self.program_type = ProgramTypeDao()
        self.banned_program = BlackSoapDao()
        self.soap_target = SoapTargetDao()
        self.heavy = HeavyTextDao()

    # def __init__(self):
    #     self.news = NewsDao()
    #     self.article = ArticleDao()
    #     self.soap = SoapDao()
    #     self.pc = PlayCountDao()
    #     self.program = ProgramDao()
    #     self.program_type = ProgramTypeDao()
    #     self.banned_program = BlackSoapDao()
    #     self.soap_target = SoapTargetDao()
    #     self.heavy = HeavyTextDao()
    #
    #     ###################################################
    #     #######   这是个隐患，最好还是给SQL操作加锁   #########
    #     ###################################################
    #     if BaseStrategy.web_order is None:
    #         BaseStrategy.web_order = self.news.get_max_order_code('web')
    #     if BaseStrategy.wechat_order is None:
    #         BaseStrategy.wechat_order = self.news.get_max_order_code('wechat')
    #     if BaseStrategy.weibo_order is None:
    #         BaseStrategy.weibo_order = self.news.get_max_order_code('weibo')
    #     if BaseStrategy.exists_url is None:
    #         BaseStrategy.exists_url = self.article.get_all_url()
    #     if BaseStrategy.exists_title is None:
    #         BaseStrategy.exists_title = self.news.get_all_title()
    #     if BaseStrategy.exists_signature is None:
    #         BaseStrategy.exists_signature = self.article.get_all_signature()
    #     if BaseStrategy.exists_identifier is None:
    #         BaseStrategy.exists_identifier = self.article.get_all_identifier()

    @staticmethod
    def init():
        news = NewsDao()
        article = ArticleDao()

        ###################################################
        #######   这是个隐患，最好还是给SQL操作加锁   #########
        ###################################################
        if BaseStrategy.web_order is None:
            BaseStrategy.web_order = news.get_max_order_code('web')
        if BaseStrategy.wechat_order is None:
            BaseStrategy.wechat_order = news.get_max_order_code('wechat')
        if BaseStrategy.weibo_order is None:
            BaseStrategy.weibo_order = news.get_max_order_code('weibo')
        if BaseStrategy.exists_url is None:
            BaseStrategy.exists_url = article.get_all_url()
        if BaseStrategy.exists_title is None:
            BaseStrategy.exists_title = news.get_all_title()
        if BaseStrategy.exists_signature is None:
            BaseStrategy.exists_signature = article.get_all_signature()
        if BaseStrategy.exists_identifier is None:
            BaseStrategy.exists_identifier = article.get_all_identifier()

    # def existsIdentifier(self):
    #     exists = self.article.get_all_signature()
    #
    #     return exists

    def store(self, news_list:[], article_list:[], heavy_list:[]=None):
        status = False

        if len(article_list) != len(news_list):
            LogGo.error("news count unmatch article count")
            return False

        count = len(news_list)
        element = 0

        if count > 0:
            if heavy_list is not None:
                for news,article,heavy in zip(news_list, article_list, heavy_list):
                    try:
                        id = genUUID()

                        self.news.save(news, id)
                        self.article.save(article, id)
                        self.heavy.save_with_news_id(heavy, id)
                        element += 1
                    except Exception as e:
                        LogGo.warning(repr(e))
            else:
                for news, article in zip(news_list, article_list):
                    try:
                        id = genUUID()

                        self.news.save(news, id)
                        self.article.save(article, id)
                        element += 1
                    except Exception as e:
                        LogGo.warning(repr(e))

            LogGo.info('Total :' + str(count) + ' / ' + str(element) + ' elements Saved!')

            if element == 0:
                status = False
            else:
                status = True
            # return True
        else:
            LogGo.info("0 Element!")
            # return False

        return status

    def store_soap(self, soap):
        status = False

        if len(soap) < 1:
            LogGo.info("no data to save!")
            return False

        try:
            id = genUUID()
            self.soap.save(soap, id)

            status = True
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

        LogGo.info('Soap Saved')

        return status

    def store_program(self, ids, programs):
        status = False

        if len(ids) != len(programs):
            LogGo.error("ids count unmatch programs count")
            return False

        count = len(ids)
        element = 0

        if count > 0:
            for id, program in zip(ids, programs):
                try:
                    self.program.save(program, id)

                    element += 1
                except Exception as e:
                    import traceback
                    msg = traceback.format_exc()
                    LogGo.warning(msg)

            LogGo.info('Total :' + str(count) + ' / ' + str(element) + ' elements Saved!')

            if element == 0:
                status = False
            else:
                status = True
        else:
            LogGo.info("0 Element!")

        return status

    def store_soap_target(self, targets:[], banned:bool=False):
        status = False
        element = 0

        for target in targets:
            try:
                if banned:
                    self.banned_program.save(target)
                else:
                    self.soap_target.save(target)

                element += 1
            except Exception as e:
                import traceback
                msg = traceback.format_exc()
                LogGo.warning(msg)

        LogGo.info('Total :' + str(element) + ' / ' + str(len(targets)) + ' elements Saved!')

        if element == 0:
            status = False
        else:
            status = True

        return status

    # def store_banned_soap_target(self, targets:[]):
    #     status = False
    #     element = 0
    #
    #     for target in targets:
    #         try:
    #             self.banned_program.save(target)
    #
    #             element += 1
    #         except Exception as e:
    #             import traceback
    #             msg = traceback.format_exc()
    #             LogGo.warning(msg)
    #
    #     LogGo.info('Total :' + str(element) + ' / ' + str(len(targets)) + ' elements Saved!')
    #
    #     if element == 0:
    #         status = False
    #     else:
    #         status = True
    #
    #     return status

    def store_program_type(self, pair):
        status = False

        count = len(pair)
        element = 0

        if count > 0:
            for item in pair:
                try:
                    program, type = item
                    self.program_type.save_by_program_type(program, type)

                    element += 1
                except Exception as e:
                    import traceback
                    msg = traceback.format_exc()
                    LogGo.warning(msg)

            LogGo.info('Total :' + str(count) + ' / ' + str(element) + ' elements Saved!')

            if element == 0:
                status = False
            else:
                status = True
        else:
            LogGo.info("0 Element!")

        return status

    def store_count(self, list):
        status = False
        count = len(list)
        element = 0
        update = 0

        if count > 0:
            for program in list:
                try:
                    if self.check_for_exists(program) == 1:
                        update += 1
                    else:
                        id = genUUID()
                        self.pc.save(program, id)

                        element += 1
                except Exception as e:
                    import traceback
                    msg = traceback.format_exc()
                    LogGo.warning(msg)

            LogGo.info('Total :' + str(count) + ' (' + str(element) + ' Saved, ' + str(update) + ' Updated)')

            if element == 0 and update == 0:
                status = False
            else:
                status = True
        else:
            LogGo.info("0 Element!")
            # return False

        return status

    def check_for_exists(self, item):
        where_dic = {}

        try:
            where_dic[TBProgramPlayCount.program.key] = item[TBProgramPlayCount.program.key]
            where_dic[TBProgramPlayCount.create_time.key] = item[TBProgramPlayCount.create_time.key]

            list = self.pc.simple_get(where_dic)

            if len(list) > 0:
                id = list[0][TBProgramPlayCount.id.key]
                count = self.pc.update(item, {TBProgramPlayCount.id.key : id})

                return 1
        except Exception as e:
            print(repr(e))

        return 0

    def gensto(self, dao, list):
        status = False
        count = len(list)
        element = 0

        if count > 0:
            for item in list:
                try:
                    id = genUUID()
                    dao.save_or_update(item, id)
                    element += 1
                except Exception as e:
                    import traceback
                    msg = traceback.format_exc()
                    # print(msg)
                    LogGo.warning(repr(e))

            LogGo.info('Total :' + str(count) + ' / ' + str(element) + ' elements Saved!')
            if element == 0:
                status = False
            else:
                status = True
        else:
            LogGo.info("0 Element!")
            stauts = False

        return status

    def genup(self, dao, list):
        status = False
        count = len(list)
        element = 0

        if count > 0:
            for (update,where) in list:
                try:
                    dao.update(update, where)

                    element += 1
                except Exception as e:
                    import traceback
                    msg = traceback.format_exc()
                    # print(msg)
                    LogGo.warning(repr(e))

            LogGo.info('Total :' + str(count) + ' / ' + str(element) + ' elements Updated!')
            if element == 0:
                status = False
            else:
                status = True
        else:
            LogGo.info("0 Element!")
            stauts = False

        return status

