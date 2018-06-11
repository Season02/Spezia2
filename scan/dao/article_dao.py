import datetime

from ...scan.entity.Target import Target

from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.date.date_go import DateGo

from Spezia2.config.global_var import Configs

from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.date.date_go import DateGo
from CoTec.core.database.GeneralDao import GeneralDao

from .DBStructure import *
from Spezia2.config.global_var import Configs


class ArticleDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBArticle()
        self.table_name = self.TB.TableName

    def get_all_url(self):
        """返回只包含 content_url 的 list """
        select_list = [self.TB.content_url.key]
        where_dic = {self.TB.is_scrabbled.key:1}

        res = self.get(self.table_name,select_list,where=where_dic)
        return res

    def get_all_signature(self):
        select = [self.TB.fingerprint.key]
        where_dic = {'<FREE>': self.TB.fingerprint.key + ' is not NULL'}

        val = self.get(self.TB.TableName, select, where=where_dic)
        return val

    def get_all_identifier(self):
        select = [self.TB.identifier.key]

        val = self.get(self.TB.TableName, select)
        return  val

    def save(self, dic:dict, id:str=None):
        return self.insert_ex(dic, self.TB.TableName, id)













#     def get_all_news(self):
#         select_list = [TBNews.id,'click_count','create_time','order_code','status','subcribe_time','text_not_format_clob','company','content_url','scrap_type','title']
#
#         val = self.get_list(self.table_name,select_list)
#         return val
#
#     def get_news(self,select, where=None,limit=None,order=None,group=None):
#         val = self.get(self.table_name, select, where, limit, order, group)
#
#         return val
#
#     def update(self, update, where):
#         sta = self.update_with_dic(self.table_name, update, where)
#         return sta
#
# def get_target_list():
#     list = []
#
#     mysql = MysqlHelper(Configs())
#     sql = "select * from scraping_target where valid = 1 order by order_code desc"
#
#     result = mysql.load(sql)
#
#     for item in result:
#
#         target = Target()
#
#         for key in item:
#             target.__dict__[key] = item[key]
#
#         list.insert(0, target)
#
#     return list
#
# def get_last_access_date(id):
#     list = []
#
#     mysql = MysqlHelper(Configs())
#     sql = "select last_access_date from scraping_target where id = '" + id + "' limit 0,1"
#
#     result = mysql.load(sql)
#
#     if len(result) > 0:
#         item = result[0]
#         item = item['last_access_date']
#
#         # print(isinstance(item, (datetime.datetime, bool)))
#         # print(type(item))
#         # print(type(datetime.datetime.date()))
#
#         if isinstance(item, (datetime.datetime, bool)):
#             return item
#         else:
#             return DateGo.get_current_date_raw()
#     else:
#         return DateGo.get_current_date_raw()
#
#
# def get_frequency(id):
#     mysql = MysqlHelper(Configs())
#     sql = "select frequency from scraping_target where id = '" + id + "' limit 0,1"
#
#     result = mysql.load(sql)
#
#     if len(result) > 0:
#         item = result[0]
#         item = item['frequency']
#
#         if isinstance(item, (int, bool)):
#             return item
#         else:
#             return 0
#     else:
#         return 0
#
#
# def set_last_access_date(id):
#     now = DateGo.get_current_date()
#
#     mysql = MysqlHelper(Configs())
#     sql = "update scraping_target set last_access_date = %s where id = %s "
#
#     mysql.execute_sql_with_par(sql,(now,id))
#
#
# def reset_target_valid(target):
#     mysql = MysqlHelper(Configs())
#     sql = "update scraping_target set valid = 0 where id = '" + target.id + "'"
#
#     mysql.update(sql)
#
#
# def test():
#     list = get_target_list()
#
#     for target in list:
#         att = dir(target)
#
#         for str in att:
#             if str == "__module__":
#                 continue
#
#             item = getattr(target, str)
#
#             if type(item) == type(str):
#                 print(str + " : " + item)

# test()

# set_last_access_date('70894E6FD22DD7A0FA92C5C26CA6A9DD')
# get_last_access_date('70894E6FD22DD7A0FA92C5C26CA6A9DD')
# rara = get_last_access_date('3ff4dff4d4')
# get_last_access_date('3ff4dff4d4')
# get_frequency('37g37g8')
# get_frequency('3ff4dff4d4')