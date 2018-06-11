from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class PNSCDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBPNSC()
        self.table_name = self.TB.TableName

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)

    def save_or_update(self, dic, id=None):
        return self.insert_or_update(dic, self.TB.TableName, id)

    def get_statistic_date(self, program_id:str) -> list:
        TB = self.TB

        select_list = [TB.current_count.key]
        where_dic = {self.TB.program.key: program_id}

        val = self.get(self.table_name, select_list, limit=None, where=where_dic)
        return val

    def get_id_by_program_id_and_date(self, program_id:str, date:str):
        select_list = [self.TB.id.key]
        where_dic = {self.TB.program.key: program_id, self.TB.create_date.key: date}

        val = self.get(self.table_name, select_list, limit=None, where=where_dic)

        if len(val) > 0:
            return val[0]