# from WS3.updatemp import Updatemp

from CoTec.core.log.log_go import LogGo
from CoTec.utility.develop.tools import Annoations

"""调用 WS3 抓取搜狗微信"""

class WS3Strategy():

    def __init__(self):
        pass

    def start(self):
        result = 0

        try:

            LogGo.info('搜狗爬虫')

            # Updatemp.loot()

            return result
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            print(msg)
            LogGo.warning(e)
            result = -1

        return result
