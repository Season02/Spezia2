import datetime

from ...scan.entity.Target import Target

from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.date.date_go import DateGo

from Spezia2.config.global_var import Configs

from Spezia2.scan.dao.DBStructure import *

def get_target_list():
    list = []

    mysql = MysqlHelper(Configs())
    # sql = "select * from scraping_target where valid = 1 and " + TBScrapingTarget.type.key + " = " + "'newrank'" + " order by order_code desc"
    sql = "select * from scraping_target where valid = 1 " + " order by order_code desc"

    result = mysql.load(sql)

    for item in result:

        target = Target()

        for key in item:
            target.__dict__[key] = item[key]

        list.insert(0, target)

    return list

def get_last_access_date(id):
    list = []

    mysql = MysqlHelper(Configs())
    sql = "select last_access_date from scraping_target where id = '" + id + "' limit 0,1"

    result = mysql.load(sql)

    if len(result) > 0:
        item = result[0]
        item = item['last_access_date']

        # print(isinstance(item, (datetime.datetime, bool)))
        # print(type(item))
        # print(type(datetime.datetime.date()))

        if isinstance(item, (datetime.datetime, bool)):
            return item
        else:
            return DateGo.get_current_date_raw()
    else:
        return DateGo.get_current_date_raw()


def get_frequency(id):
    mysql = MysqlHelper(Configs())
    sql = "select frequency from scraping_target where id = '" + id + "' limit 0,1"

    result = mysql.load(sql)

    if len(result) > 0:
        item = result[0]
        item = item['frequency']

        if isinstance(item, (int, bool)):
            return item
        else:
            return 0
    else:
        return 0


def set_last_access_date(id:str):
    now = DateGo.get_current_date()

    mysql = MysqlHelper(Configs())
    sql = "update scraping_target set last_access_date = %s where id = %s "

    mysql.execute_sql_with_par(sql,(now,id))


def set_last_failed_time(id:str):
    now = DateGo.get_current_date()

    mysql = MysqlHelper(Configs())
    sql = "update " + TBScrapingTarget.TableName + " set " + TBScrapingTarget.last_failed_time.key + " = %s where id = %s "

    mysql.execute_sql_with_par(sql, (now, id))


def set_elog(id:str, elog) -> ():
    mysql = MysqlHelper(Configs())
    sql = "update " + TBScrapingTarget.TableName + " set " + TBScrapingTarget.elog.key + " = %s where id = %s "

    mysql.execute_sql_with_par(sql, (str(elog), id))

    set_last_failed_time(id)


def reset_target_valid(target):
    mysql = MysqlHelper(Configs())
    sql = "update scraping_target set valid = 0 where id = '" + target.id + "'"

    mysql.update(sql)


def test():
    list = get_target_list()

    for target in list:
        att = dir(target)

        for str in att:
            if str == "__module__":
                continue

            item = getattr(target, str)

            if type(item) == type(str):
                print(str + " : " + item)

