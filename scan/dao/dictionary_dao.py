from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs
from CoTec.utility.string.string_go import genUUID


class DictionaryDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBDictionary()
        self.table_name = self.TB.TableName

    # def update(self, update, where):
    #     sta = self.update_with_dic(self.table_name, update, where)
    #     return sta
    #

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)

    def save_by_type_title(self, type_id, title):
        dic = {self.TB.title.key:title, self.TB.valid.key:'1', self.TB.dic_type_id.key:type_id}
        id = genUUID()

        if self.save(dic, id):
            return id

    def get_id_by_type_title(self, type_id:str, title_str:str):
        where_dic = {self.TB.title.key: title_str, self.TB.dic_type_id.key: type_id}
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


