from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class NewsDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBNews()
        self.STB = TBArticle()
        self.table_name = self.TB.TableName

    def get_all_title(self):
        select = [self.TB.title.key]
        sub_table = TBArticle()
        sub_where = {sub_table.is_scrabbled.key:1}
        # where = {'<IN>' + self.TB.id.key:'select ' + self.TB.id.key + ' from ' + sub_table.TableName + ' where ' + sub_table.is_scrabbled.key + ' =1'}
        where = {'<IN>' + self.TB.id.key: [sub_table.TableName, sub_where]}
        val = self.get(self.TB.TableName, select, where)
        return val

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta

    def get_max_order_code(self, type):
        select = 'n.' + TBNews.order_code.key
        from_sql = TBNews.TableName + ' as n,' + TBArticle.TableName + ' as a '
        where = 'n.' + TBNews.id.key + ' = a.' + TBArticle.id.key + ' and a.' + TBArticle.scrabble_type.key + ' ="' + type + '"'
        limit = (0,1)
        order = ('n.' + TBNews.order_code.key, 'desc')

        result = self.get_by_sqls(select,from_sql,where,limit,order)

        if result is None:
            return 0

        if len(result) > 0:
            item = result[0]
            return int(item[TBNews.order_code.key])
        else:
            return 0

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName, id)

