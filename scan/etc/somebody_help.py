from CoTec.core.request.request_go import RequestHelper

from CoTec.utility.date.date_go import DateGo

from CoTec.utility.string.string_go import genUUID

from ...config.global_var import Configs
from CoTec.utility.file.file_go import FileHelper
from CoTec.utility.string.string_go import StringHelper
from CoTec.core.log.log_go import LogGo

import  threading

class somebody_help():
    """各种小的帮助类"""

    @staticmethod
    def update_index():
        def get_request():
            url = 'http://app.media-plus.cn/portal/search/updateIndex'
            RequestHelper.get(url)

        try:
            t = threading.Thread(target=get_request)
            t.daemon = True
            t.start()
        except Exception:
            pass

    @staticmethod
    def isthataworkday(record:list) -> bool:
        """
        [(8,9), (12,14), (16,18), (20,22)]
        :param record:
        :return:
        """
        current_hour = int(DateGo.get_current_hour())

        for duration in record:
            if current_hour in range(duration[0], duration[1]):
                return True

        return False

    @staticmethod
    def check_shutdown_status():
        try:
            file_name = Configs().system_shutdown_flag_filename

            status = int(StringHelper.trim(FileHelper.read(file_name)))

            if status == 1:
                somebody_help.reset_shutdown_status()
                return True
            else:
                return False
        except:
            LogGo.error("system_shutdown_flag_file unavailable!")
            return False

    @staticmethod
    def set_shutdown_status():
        try:
            file_name = Configs().system_shutdown_flag_filename

            FileHelper.create(file_name, "1")
        except:
            LogGo.error("something wrong at setting shutdown flag file !!!")

    @staticmethod
    def reset_shutdown_status():
        try:
            file_name = Configs().system_shutdown_flag_filename

            FileHelper.create(file_name, "0")
        except:
            LogGo.error("error while reseting shutdown flag file!!!")



# print(somebody_help.isthataworkday(list))



