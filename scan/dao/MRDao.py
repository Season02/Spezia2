from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class MRDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBMR()
        self.table_name = self.TB.TableName

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)



