from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class HeavyTextDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBHeavyText()
        self.table_name = self.TB.TableName

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta

    def save_with_news_id(self, dic: dict, news_id: str):
        dic[self.TB.news_id.key] = news_id

        return self.insert_ex(dic, self.TB.TableName)







