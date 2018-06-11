from Spezia2.config.global_var import Configs
from abc import abstractmethod

class BaseRuler():
    # def __init__(self):
    #     pass

    @abstractmethod
    def scan_list(self, target, exists) -> (int, ()):
        pass

    @abstractmethod
    def scan_detail(self, target, detail_page_bundle, order, content_ruler, encode) -> dict:
        pass

    def ready_info(self, title, link):
        if Configs.show_utf:
            title = title
        else:
            title = ''

        result = title + "(" + link + ")"

        return result
