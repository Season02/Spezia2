from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class PlayCountDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBProgramPlayCount()
        self.table_name = self.TB.TableName

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)

    def simple_get(self, where_dic):
        select_list = [self.TB.id.key]

        list = self.get_list(self.table_name, select_list=select_list, where_dic=where_dic)

        return list

