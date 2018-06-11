import datetime

from ...scan.entity.Target import Target

from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.date.date_go import DateGo
from CoTec.core.database.GeneralDao import GeneralDao

from Spezia2.config.global_var import Configs

from .DBStructure import *

class BlackSoapDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBSoapBlackList
        self.table_name = self.TB.TableName

    def get_id_by_type(self, soap_type:str):
        where_dic = {self.TB.valid.key: 1, self.TB.type.key: soap_type}
        select_list = [self.TB.program.key]

        val = self.get(self.table_name, select_list, limit=None, where=where_dic)

        return val[0]

    def save(self, dic:dict, id:str=None):
        return self.insert_ex(dic, self.TB.TableName)

