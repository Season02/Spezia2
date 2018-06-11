import datetime
from CoTec.core.database.GeneralDao import GeneralDao
from ...scan.entity.Target import Target

from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.date.date_go import DateGo

from Spezia2.config.global_var import Configs

from Spezia2.scan.dao.DBStructure import *

class SpecialTargetDao(GeneralDao):

    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.table = TBSpecialTarget()
        self.table_name = self.table.TableName

    def save(self, dic: dict, id: str = None):
        return self.insert_ex(dic, self.table_name, id)

    def set_last_access_date(self, id):
        now = DateGo.get_current_date()
        dic = {self.table.last_access_date.key:now}
        where = {self.table.id.key: id}

        return self.update_with_dic(self.table_name, dic, where)

    def get_target_list(self) -> []:
        list = []

        sql = "select * from " + self.table_name + " where " + self.table.valid.key + " = 1 " + " order by " + self.table.order_code.key + " desc"

        result = self.mysql.load(sql)

        for item in result:

            target = Target()

            for key in item:
                target.__dict__[key] = item[key]

            list.insert(0, target)

        return list

    def get_last_access_date(self, id):
        sql = "select " + self.table.last_access_date.key + " from " + self.table_name + " where " + self.table.id.key + " = '" + id + "' limit 0,1"

        result = self.mysql.load(sql)

        if len(result) > 0:
            item = result[0]
            item = item[self.table.last_access_date.key]

            if isinstance(item, (datetime.datetime, bool)):
                return item
            else:
                return DateGo.get_current_date_raw()
        else:
            return DateGo.get_current_date_raw()

    def get_frequency(self, id):
        sql = "select " + self.table.frequency.key + " from " + self.table.frequency.key + " where " + self.table.id.key + " = '" + id + "' limit 0,1"

        result = self.mysql.load(sql)

        if len(result) > 0:
            item = result[0]
            item = item['frequency']

            if isinstance(item, (int, bool)):
                return item
            else:
                return 0
        else:
            return 0

    def set_last_failed_time(self, id: str):
        now = DateGo.get_current_date()

        sql = "update " + self.table_name + " set " + self.table.last_failed_time.key + " = %s where id = %s "

        self.mysql.execute_sql_with_par(sql, (now, id))

    def set_elog(self, id: str, elog) -> ():
        sql = "update " + self.table_name + " set " + self.table.elog.key + " = %s where id = %s "

        self.mysql.execute_sql_with_par(sql, (str(elog), id))

        self.set_last_failed_time(id)

    def reset_target_valid(self, target):
        sql = "update scraping_target set valid = 0 where id = '" + target.id + "'"

        self.mysql.update(sql)
