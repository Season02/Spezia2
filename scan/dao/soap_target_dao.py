import datetime

from ...scan.entity.Target import Target

from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.date.date_go import DateGo
from CoTec.core.database.GeneralDao import GeneralDao

from Spezia2.config.global_var import Configs

from .DBStructure import *

class SoapTargetDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBSoapTarget()
        self.table_name = self.TB.TableName

    def get_target_list(self):
        list = []

        mysql = MysqlHelper(Configs())
        sql = "select * from " + self.table_name + " where " + self.TB.valid.key + " = 1 order by " + self.TB.order_code.key + " desc"

        result = mysql.load(sql)

        for item in result:

            target = Target()

            for key in item:
                target.__dict__[key] = item[key]

            list.insert(0, target)

        return list

    def get_last_access_date(self, id):
        list = []

        mysql = MysqlHelper(Configs())
        sql = "select " + self.TB.last_access_date.key + " from " + self.table_name + " where " + self.TB.id.key + " = '" + id + "' limit 0,1"

        result = mysql.load(sql)

        if len(result) > 0:
            item = result[0]
            item = item[self.TB.last_access_date.key]

            # print(isinstance(item, (datetime.datetime, bool)))
            # print(type(item))
            # print(type(datetime.datetime.date()))

            if isinstance(item, (datetime.datetime, bool)):
                return item
            else:
                return DateGo.get_current_date_raw()
        else:
            return DateGo.get_current_date_raw()

    def get_frequency(self, id):
        mysql = MysqlHelper(Configs())
        sql = "select " + self.TB.frequency.key + " from " + self.table_name + " where " + self.TB.id.key + " = '" + id + "' limit 0,1"

        result = mysql.load(sql)

        if len(result) > 0:
            item = result[0]
            item = item[self.TB.frequency.key]

            if isinstance(item, (int, bool)):
                return item
            else:
                return 0
        else:
            return 0


    def set_last_access_date(self, id):
        now = DateGo.get_current_date()

        mysql = MysqlHelper(Configs())
        sql = "update " + self.table_name + " set " + self.TB.last_access_date.key + " = %s where " + self.TB.id.key + " = %s "

        mysql.execute_sql_with_par(sql,(now,id))


    def reset_target_valid(self, target):
        mysql = MysqlHelper(Configs())
        sql = "update " + self.table_name + " set " + self.TB.valid.key + " = 0 where " + self.TB.id.key + " = '" + target.id + "'"

        mysql.update(sql)

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.TB.TableName)


