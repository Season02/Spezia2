from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class SoapDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBSoap()
        self.table_name = self.TB.TableName

    # def get_all_title(self):
    #     select = [self.TB.title.key]
    #     sub_table = TBArticle()
    #     sub_where = {sub_table.is_scrabbled.key:1}
    #     # where = {'<IN>' + self.TB.id.key:'select ' + self.TB.id.key + ' from ' + sub_table.TableName + ' where ' + sub_table.is_scrabbled.key + ' =1'}
    #     where = {'<IN>' + self.TB.id.key: [sub_table.TableName, sub_where]}
    #     val = self.get(self.TB.TableName, select, where)
    #     return val

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)

    def get_new_count(self):
        sql = 'select t.' + TBSoap.play_count.key + ',t.' + TBSoap.program.key + ',t.' + TBSoap.plantform.key + ' from (select ' + '*' + ' from ' + TBSoap.TableName + ' order by ' + TBSoap.create_date.key + ') t group by t.' + TBSoap.target.key
        # sql = 'select * from ' + TBSoap.TableName + ' where ' + TBSoap.id.key + ' in(select SUBSTRING_INDEX(group_concat(' + TBSoap.id.key + ' order by ' + TBSoap.create_date.key + " desc),',',1) from " + TBSoap.TableName + ' group by ' + TBSoap.target.key + ' ) order by ' + TBSoap.create_date.key + ' desc'

        res = self.load(sql)
        return res

    def get_max_order_code(self):
        select_list = [self.TB.order_code.key]
        order_tup = (self.TB.order_code.key, 'desc')
        limit = (0, 1)

        res = self.get(self.table_name, select_list, order=order_tup, limit=limit)

        if len(res) > 0:
            item = res[0]
            return item
        else:
            return 0


