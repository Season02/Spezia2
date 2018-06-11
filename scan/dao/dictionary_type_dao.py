from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class DictionaryTypeDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBDictionaryType()
        self.table_name = self.TB.TableName

    # def update(self, update, where):
    #     sta = self.update_with_dic(self.table_name, update, where)
    #     return sta
    #
    # def save(self, id, dic):
    #     return self.insert(self.TB.TableName, id, dic)

    def get_id_by_code(self, code):
        where_dic = {self.TB.code.key: code}
        select_list = [self.TB.id.key]
        limit = (0, 1)

        val = self.get(self.table_name, select_list, limit=limit, where=where_dic)

        if len(val) > 0:
            return val[0]

    # def get_max_order_code(self):
    #     select_list = [self.TB.order_code.key]
    #     order_tup = (self.TB.order_code.key, 'desc')
    #     limit = (0, 1)
    #
    #     res = self.get(self.table_name, select_list, order=order_tup, limit=limit)
    #
    #     if len(res) > 0:
    #         item = res[0]
    #         return item
    #     else:
    #         return 0


