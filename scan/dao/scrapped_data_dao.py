from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.string.string_go import genUUID
from .DBStructure import *

from Spezia2.config.global_var import Configs

tableName = 'news'
article_table_name = 'article'

class ScrappdeDataDao:
    news = TBNews()
    news_table_name = news.TableName
    article_table_name = 'article'

    # def __init__(self):
    #     GeneralDao.__init__(self, Configs())
    #
    #     self.table_name = self.news.TableName

    # def get_all_news(self):
    #     select_list = [TBNews.id, 'click_count', 'create_time', 'order_code', 'status', 'subcribe_time',
    #                    'text_not_format_clob', 'company', 'content_url', 'scrap_type', 'title']
    #
    #     val = self.get_list(self.table_name, select_list)
    #     return val

    """返回只包含 content_url 的 list """
    @staticmethod
    def get_all_url():
        list = []

        mysql = MysqlHelper(Configs())
        sql = "select `content_url` from news where is_scrapped = 1"

        result = mysql.load(sql)

        for item in result:
            list.append(item['content_url'])

        if len(list) < 1:
            list.append('QWERTYUIOP')

        return list

    @staticmethod
    def get_all_title():
        list = []

        mysql = MysqlHelper(Configs())
        sql = "select `title` from news where is_scrapped = 1"

        result = mysql.load(sql)

        for item in result:
            list.append(item['title'])

        if len(list) < 1:
            list.append('QWERTYUIOP')

        return list

    # @staticmethod
    # def get_all_signature():
    #     list = ScrappdeDataDao.get_all_value_for_key(ScrappdeDataDao.news.fingerprint.key)
    #
    #     return list

    @staticmethod
    def get_all_identifier():
        list = ScrappdeDataDao.get_all_value_for_key('identifier')

        return list

    @staticmethod
    def get_all_value_for_key(key):
        list = []

        mysql = MysqlHelper(Configs())

        sql = "select `" + str(key) + "` from news where is_scrapped = 1 and " + str(key) + " is not null"

        result = mysql.load(sql)

        for item in result:
            list.append(item[str(key)])

        if len(list) < 1:
            list.append('QWERTYUIOP')

        return list

    @staticmethod
    def dic_to_sql_part(dic):
        res = ''
        for key in dic:
            res += key
            res += ' = "'
            res += dic[key]
            res += '" and '

        res += '1=1'

        return res

    @staticmethod
    def list_to_sql_part(list):
        res = ''
        for item in list:
            res += item
            res += ','

        res = res[0: len(res) - 1]

        return res

    @staticmethod
    def part_dic_to_update_sql(dic):
        sql = ''
        for key in dic:
            if key != 'id':
                sql += key
                sql += ' = '
                sql += str(dic[key])
                sql += ','

        sql = sql[0: len(sql) - 1]
        return sql

    @staticmethod
    def update_with_dic(dic):
        mysql = MysqlHelper(Configs())
        update_sql = ScrappdeDataDao.part_dic_to_update_sql(dic)
        sql = "update " + tableName + " set " + update_sql + " where id = '" + dic['id'] + "'"

        mysql.update(sql)

    @staticmethod
    def par_to_get_dic(select_list, and_dic, order_key = None, limit_tup = None):
        list = []
        select_sql = ScrappdeDataDao.list_to_sql_part(select_list)
        and_sql = ScrappdeDataDao.dic_to_sql_part(and_dic)
        if order_key != None:
            order_key = ' order by ' + order_key[0] + ' ' + order_key[1]
        else:
            order_key = ''
        if limit_tup != None:
            limit_tup = ' limit ' + str(limit_tup[0]) + ',' + str(limit_tup[1])
        else:
            limit_tup = ''

        mysql = MysqlHelper(Configs())
        sql = "select " + select_sql + " from " + tableName + " where is_scrapped = 1 and " + and_sql + " " + order_key + limit_tup

        result = mysql.load(sql)

        for item in result:
            list.append(item)

        return list

    @staticmethod
    def get_max_order_code():
        list = []

        mysql = MysqlHelper(Configs())
        sql = "select `order_code` from news where is_scrapped = 1 order by `order_code` desc limit 0,1"

        result = mysql.load(sql)

        if len(result) > 0:
            item = result[0]
            return int(item['order_code'])
        else:
            return 0

    @staticmethod
    def get_max_order(type):
        list = []

        mysql = MysqlHelper(Configs())
        sql = "select `order_code` from news where is_scrapped = 1 and scrap_type = '" + type + "' order by `order_code` desc limit 0,1"

        result = mysql.load(sql)

        if result is None:
            return 0

        if len(result) > 0:
            item = result[0]
            return int(item['order_code'])
        else:
            return 0

    @staticmethod
    def save_data(dic):
        dis = ""

        id = genUUID()

        for key in dic:
            dis += key
            dis += "='"
            dis += str(dic[key])
            dis += "',"

        dis = dis[0: len(dis) - 1]

        mysql = MysqlHelper(Configs())

        sql = "insert into news set id=%s,"
        sql += dis
        mysql.save(sql, id)

        sql = "insert into "
        sql += article_table_name
        sql += " set id=%s"
        mysql.save(sql, id)

    @staticmethod
    def save_data_insert(dic):

        id = genUUID()

        mysql = MysqlHelper(Configs())

        _sql = "INSERT INTO news(`id`, "
        _val = " VALUES (%s,"
        _par = [id,]

        for key in dic:
            _sql += "`"
            _sql += key
            _sql += "`,"

            if type(dic[key]) == type(str):
                _val += "%s,"
            elif type(dic[key]) == type(int):
                _val += "%i,"
            else:
                _val += "%s,"

            _par.append(dic[key])

        _sql = _sql[0: len(_sql) - 1]
        _sql += ")"

        _val = _val[0: len(_val) - 1]
        _val += ")"

        _sql += _val

        mysql.save(_sql, _par)

        sql = "insert into "
        sql += article_table_name
        sql += " set id=%s"
        mysql.save(sql, id)


    def test(self):
        par = "content_url='0000',title='0000',type='0000'"

        self.save_data(par)
