from ...scan.ruler.ulweb import UlWebRuler
# from ...scan.dao.scrapped_data_dao import ScrappdeDataDao
from .BaseStrategy import BaseStrategy

from CoTec.core.exception.exception_go import *

from CoTec.core.log.log_go import LogGo

class WebStrategy(BaseStrategy):
    #访问失败的详情页信息
    temp_list = []

    def __init__(self):
        BaseStrategy.__init__(self)

        # ###################################################
        # #######   这是个隐患，最好还是给SQL操作加锁   #########
        # ###################################################
        # if WebStrategy.web_order is None:
        #     WebStrategy.web_order = self.news.get_max_order_code('web')
        # if WebStrategy.exists_url is None:
        #     WebStrategy.exists_url = self.article.get_all_url()

        # self.web_order = WebStrategy.web_order
        # self.exists_url = WebStrategy.exists_url

    def scrape_list(self, target):
        LogGo.info("On scrape list: " + str(target.data_key))

        try:
            exists = self.exists_url

            ulweb = UlWebRuler()
            code, value = ulweb.scan_list(target, exists)

            return (code, value)
        except WebTargetOutOfDateException as e:
            LogGo.warning(e.args[0])
        except Exception as e:
            import traceback
            LogGo.warning(repr(e))

        return (0, None)

    def scrape_detail(self, target, detail_page_bundle, content_ruler, encode):
        try:
            order = self.web_order

            ulweb = UlWebRuler()
            result = ulweb.scan_detail(target, detail_page_bundle, order, content_ruler, encode)

            code, detail_page_result = result

            if code == 1:
                if detail_page_result is not None:
                    return (1, detail_page_result)
            elif code == -3:
                self.temp_list.append((target, detail_page_bundle, content_ruler, encode))

        except WebTargetOutOfDateException as e:
            return (-1, e.args[0])
        except Exception as e:
            import traceback
            LogGo.warning(repr(e))
            return (-1, e.args[0])

        return (0, None)
