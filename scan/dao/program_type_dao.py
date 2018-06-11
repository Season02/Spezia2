from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs
from CoTec.utility.string.string_go import genUUID


class ProgramTypeDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBProgramType()
        self.table_name = self.TB.TableName

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)

    def save_by_program_type(self, program_id, type_id):
        dic = {self.TB.programId.key:program_id, self.TB.typeId.key:type_id}
        id = genUUID()

        if self.save(dic, id):
            return id

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


