from CoTec.core.database.GeneralDao import GeneralDao
from Spezia2.config.global_var import Configs

from .DBStructure import *

class ProgramDao(GeneralDao):

    def __init__(self):


        self.TB = TBProgram()
        self.table_name = self.TB.TableName

        GeneralDao.__init__(self, Configs())

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)

    def get_all_title_cn(self):
        TB = self.TB

        select_list = [TB.title_cn.key]
        where_dic = {'<FREE>': self.TB.title_cn.key + ' is not NULL'}

        val = self.get(self.table_name, select_list, limit=None, where=where_dic)
        return val

    def get_all_title_by_type(self, type):
        TB = self.TB

        select_list = [TB.title_cn.key]
        where_dic = {self.TB.type.key:str(type), '<FREE>': self.TB.title_cn.key + ' is not NULL'}

        val = self.get(self.table_name, select_list, limit=None, where=where_dic)
        return val

    def get_all_program(self):
        TB = self.TB

        where_dic = {self.TB.valid.key: '1'}
        select_list = [TB.title_cn.key, TB.id.key]
        limit = (1,1)

        val = self.get(self.table_name, select_list, limit=None, where=where_dic)
        return val

    def get_title_by_id(self, id):
        TB = self.TB

        where_dic = {self.TB.id.key:id}
        select_list = [TB.title_cn.key]
        limit_tup = (0,1)

        title = self.get(self.table_name, select_list, where=where_dic, limit=limit_tup, ex=True)
        return title

    def get_no_soap_program_id_by_type(self, soap_type:str):
        """
        获取没有记录在 soap_target 中的 对应 type 为 soap_type 的 program id
        :param soap_type: youku y c cntv i iqiyi l le lety m mgtv q qq s sohu souhu t
        :return:
        """

        # sql = "select id from program where id not in (select program_id from soap_target where program_id is not null and soap_type = '" + soap_type + "') and type != 2"
        inwhere_sql = "id not in (select program_id from soap_target where program_id is not null and soap_type = '" + soap_type + "') and type != 2"

        select = [self.TB.id.key]
        where_dic = {'<FREE>': inwhere_sql}

        val = self.get(self.TB.TableName, select, where=where_dic)
        return val

    def get_no_soap_program_id_title_by_type(self, soap_type:str):
        """
        获取没有记录在 soap_target 中的 对应 type 为 soap_type 的 program id
        :param soap_type: youku y c cntv i iqiyi l le lety m mgtv q qq s sohu souhu t
        :return:
        """

        # inwhere_sql = "id not in (select program_id from soap_target where program_id is not null and soap_type = '" + soap_type + "') and type != 2 and valid = 1"
        inwhere_sql = "id not in (select program_id from soap_target where program_id is not null and soap_type = '" + soap_type + "') and id not in (select program_id from soap_black_list where valid = 1 and soap_type = '" + soap_type + "') and type != 2 and valid = 1"

        select = [self.TB.id.key, self.TB.title_cn.key, self.TB.type.key]
        where_dic = {'<FREE>': inwhere_sql}

        val = self.get(self.TB.TableName, select, where=where_dic)
        return val






