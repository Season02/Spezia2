from ...scan.ruler.newrank import NewrankRuler
from ...scan.ruler.wechat import WechatRuler
# from ...scan.ruler.sogou_transfor import SougouTransforRuler
from ...scan.ruler.gsdata import GsdataRuler
# from ...scan.dao.scrapped_data_dao import ScrappdeDataDao
from ...scan.dao.article_dao import ArticleDao
from ...scan.dao.news_dao import NewsDao

from CoTec.core.log.log_go import LogGo
from CoTec.core.SMTP.smtp_go import SMTPServer
from CoTec.core.request.request_go import RequestHelper

from CoTec.utility.string.string_go import genUUID

from .BaseStrategy import BaseStrategy


"""这里应该是有很多方案，很多替补，有检测环节，一个方案失败或没有结果，自动化的查明原因后自动修正并在需要时切换为其它提取方案"""
class WechatStrategy(BaseStrategy):

    temp_list = []

    def __init__(self):
        BaseStrategy.__init__(self)

    def newrank_list(self, target):
        LogGo.info("On newrank list: " + str(target.data_key))

        try:
            exists = self.exists_title

            newrank = NewrankRuler()
            code, value = newrank.scan_list(target, exists)

            return (code, value)
        except Exception as e:
            import traceback
            LogGo.warning(repr(e))

            return (0, None)

    def newrank_detail(self, target, detail_page_bundle, content_ruler, encode):
        LogGo.info("On newrank detail: " + str(target.data_key))

        try:
            order = self.wechat_order

            newrank = NewrankRuler()
            result = newrank.scan_detail(target, detail_page_bundle, order, content_ruler, encode)

            code, detail_page_result = result

            if code == 1:
                if detail_page_result is not None:
                    return (1, detail_page_result)
            elif code == -3:
                self.temp_list.append((target, detail_page_bundle, content_ruler, encode))

        except Exception:
            LogGo.warning('error in newrank detail')
            return (-1, None)

        return (0, None)

    def gs_list(self, target):
        LogGo.info("On gs list: " + str(target.data_key))

        try:
            exists = self.exists_signature

            gs = GsdataRuler()
            code, value = gs.scan_list(target, exists)

            return (code, value)
        except Exception as e:
            import traceback
            LogGo.warning(repr(e))

        return (0, None)

    def gs_detail(self, target, detail_page_bundle, content_ruler, encode):
        LogGo.info("On gs detail: " + str(target.data_key))

        try:
            order = self.wechat_order

            gs = GsdataRuler()
            result = gs.scan_detail(target, detail_page_bundle, order, content_ruler, encode)

            code, detail_page_result = result

            if code == 1:
                if detail_page_result is not None:
                    return (1, detail_page_result)
            elif code ==3:
                self.temp_list.append((target, detail_page_bundle, content_ruler, encode))

        except Exception as e:
            import traceback
            LogGo.warning(repr(e))
            return (-1, e.args[0])

        return (0, None)

    def ScanWechatTarget(self, target):

        result = 0

        # existsUrls = ScrappdeDataDao.get_all_url()
        existsUrls = self.article.get_all_url()# ScrappdeDataDao.get_all_url()
        order = self.news.get_max_order_code('wechat')

        wechat = WechatRuler()

        news, article = wechat.ExtraList(target, existsUrls, order)

        content = '微信(Wechat)任务(' + target.data_key + ')' + '\r\n'
        content += '此次采集数量: ' + str(len(news)) + '\r\n'

        if self.store(news,article):
            result = 1
        else:
            # LogGo.info(" No New Element!")
            result = -1

        if result == 1:
            content += '存储成功!'

        SMTPServer.build_mission_report(content)

        return result

    def sogou_transfor(self):

        LogGo.info('搜狗转移')

        result = 0

        # sogou = SougouTransforRuler()
        #
        # existsUrls = self.news.get_all_title()
        # order = self.news.get_max_order_code('wechat')
        #
        # news, article = sogou.ExtraList(existsUrls, order)
        #
        # content = '搜狗转移任务(' + ')' + '\r\n'
        # content += '此次采集数量: ' + str(len(news)) + '\r\n'
        #
        # if self.store(news, article):
        #     result = 1
        # else:
        #     result = -1
        #
        # if result == 1:
        #     content += '存储成功!'
        #
        # SMTPServer.build_mission_report(content)
        # print(content)

        return result

class Helper:

    @staticmethod
    def unifyurl(url):
        from urllib.parse import urlparse

        part = urlparse(url)
        url = part.geturl()
        return url



