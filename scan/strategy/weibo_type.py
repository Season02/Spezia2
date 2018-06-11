from ...scan.ruler.weibo import WeiboRuler

from CoTec.core.log.log_go import LogGo
from CoTec.utility.develop.tools import Annoations
from CoTec.core.SMTP.smtp_go import SMTPServer

from .BaseStrategy import BaseStrategy

"""这里应该是有很多方案，很多替补，有检测环节，一个方案失败或没有结果，自动化的查明原因后自动修正并在需要时切换为其它提取方案"""


class WeiboStrategy(BaseStrategy):

    def __init__(self):
        BaseStrategy.__init__(self)

    def weibo_list(self, target):
        LogGo.info("On weibo list: " + str(target.data_key))

        try:
            exists = self.exists_identifier

            weibo = WeiboRuler()
            code, value = weibo.scan_list(target, exists)

            return (code, value)
        except Exception as e:
            import traceback
            LogGo.warning(repr(e))

        return (0, None)

    def weibo_detail(self, target, detail_page_bundle, content_ruler, encode):
        LogGo.info("On weibo detail: " + str(target.data_key))

        try:
            order = self.weibo_order

            weibo = WeiboRuler()
            detail_page_result_dic = weibo.scan_detail(target, detail_page_bundle, order, content_ruler, encode)

            if detail_page_result_dic is not None:
                return (1, detail_page_result_dic)
        except Exception as e:
            import traceback
            LogGo.warning(repr(e))
            return (-1, e.args[0])

        return (0, None)

    # def scan_weibo(self, target, exists_program:list):
    #
    #     result = 0
    #
    #     try:
    #         # exists_ids = ScrappdeDataDao.get_all_identifier()
    #         exists_ids = self.article.get_all_identifier()
    #         order = self.news.get_max_order_code('weibo')
    #
    #         weibo = WeiboRuler()
    #
    #         content = '微博任务(' + target.data_key + ')' + '\r\n'
    #
    #         res = weibo.scan(target, exists_ids, order, exists_program)
    #
    #         if res is not None:
    #             news, article = res
    #
    #             content += '此次采集数量: ' + str(len(article)) + '\r\n'
    #
    #             if self.store(news, article):
    #                 result = 1
    #             else:
    #                 result = -1
    #
    #             if result == 1:
    #                 content += '存储成功!'
    #         else:
    #             content += '此次采集数量: ' + str(0) + '\r\n'
    #
    #         SMTPServer.build_mission_report(content)
    #
    #         return result
    #     except Exception as e:
    #         import traceback
    #         msg = traceback.format_exc()
    #         print(msg)
    #         LogGo.warning(e)
    #         result = -1
    #
    #     return result
