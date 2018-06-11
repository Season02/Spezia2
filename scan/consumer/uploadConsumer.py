from .baseConsumer import base_consumer
from ..queue.uploadQueue import upload_queue
import threading
from CoTec.utility.date.date_go import DateGo
from ...scan.strategy.web_type import WebStrategy
import json

from CoTec.core.request.request_go import RequestHelper
from ...config.global_var import Configs

from CoTec.core.exception.exception_go import ExceptionGo as E
from CoTec.core.log.log_go import LogGo


class upload_consumer(threading.Thread):
    """
    拿到 一个页面的 result 转换为 对应 json 发送请求
    """
    def __init__(self, queue_size):
        super().__init__()
        self.upload_queue = upload_queue(queue_size)
        self.base = base_consumer()

    def run(self):
        while True:
            # print("upload queue unfinishd count: " + str(self.queue.queue.unfinished_tasks))
            result_dic = self.upload_queue.queue.get()  # 当队列为空时，会阻塞，直到有数据

            self.base.get_thread(self.send_request, result_dic)

            # LogGo.info("Posting Message")

            self.upload_queue.queue.task_done()

    def send_request(self, result_dic):
        json_dic = dict()
        json_dic['date'] = DateGo.get_current_date()
        json_dic['targetId'] = 'No Target ID!'
        json_dic['rowList'] = [result_dic]

        try:
            LogGo.info("Ready to Post!")

            raw = RequestHelper.post(Configs.fish_data_post_url, json = json_dic)

            preview_dic = result_dic.copy()
            preview_dic['text_not_format_clob'] = 'DUMMY CONTENT'
            preview_dic['text_blob'] = 'DUMMY CONTENT'
            json_dic['rowList'] = preview_dic

            json_str = json.dumps(json_dic)

            LogGo.info("POST CONTENT: " + json_str)
            LogGo.info("POST RESPONSE: " + str(raw))
        except Exception:
            E.out_err()






