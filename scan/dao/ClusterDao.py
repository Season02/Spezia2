from CoTec.core.database.GeneralDao import GeneralDao
from CoTec.utility.string.string_go import StringHelper as SH

from .DBStructure import *
from ...config.global_var import Configs

class ClusterDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBNewsGroup()
        self.table_name = self.TB.TableName

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta

    # def get_all_keywords(self):
    #     """返回只包含 content_url 的 list """
    #     select_list = [TBNewsGroup.id.key, TBNewsGroup.keywords.key, TBNewsGroup.abstract.key, TBNewsGroup.title.key]
    #     where_dic = {TBNewsGroup.valid.key:'1', '<FREE>': TBNewsGroup.keywords.key + ' IS NOT NULL'}
    #
    #     res = self.get(self.table_name,select_list,where=where_dic)
    #     return res

    def get_all_cluster(self):
        TB = self.TB

        # where_dic = {TBNewsGroup.valid.key: '1', '<FREE>': TBNewsGroup.statistics_date.key + ' IS NULL'}
        # where_dic = {'<FREE>': TBNewsGroup.statistics_date.key + ' IS NULL'} WHY WHY WHY WHY WHY
        where_dic = {TBNewsGroup.valid.key: '1'}
        select_list = [TB.title.key, TB.id.key]
        limit = (0,4)

        val = self.get(self.table_name, select_list, limit=None, where=where_dic)
        return val

    def save(self, dic:dict, id:str=None):
        return self.insert_ex(dic, self.TB.TableName, id)

