from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.string.string_go import genUUID
from .group_picture_dao import GroupPictureDao

from Spezia2.config.global_var import Configs

tableName = 'picture'

class PictureDao:

    """返回只包含 content_url 的 list """
    # @staticmethod
    # def get_all_url():
    #     list = []
    #
    #     mysql = MysqlHelper()
    #     sql = "select `content_url` from news"
    #
    #     result = mysql.load(sql)
    #
    #     for item in result:
    #         list.append(item['content_url'])
    #
    #     return list



    def save_data(self,url):

        id = genUUID()
        name = genUUID() + ".jpg"

        dic = dict()
        dic['filename'] = name
        dic['min_path'] = url
        dic['normal_path'] = url
        dic['origin_filename'] = name
        dic['valid'] = 1

        dis = ""

        for key in dic:
            dis += key
            dis += "='"
            dis += str(dic[key])
            dis += "',"

        dis = dis[0: len(dis) - 1]

        mysql = MysqlHelper(Configs())

        sql = "insert into "
        sql += tableName
        sql += " set id=%s,"
        sql += dis
        mysql.save(sql, id)

        return id

    @staticmethod
    def save_group_data(list):
        if len(list) < 1:
            return None

        dao = PictureDao()
        group_id = genUUID()
        ids = []

        for pic in list:
            ids.append(dao.save_data(pic))

        for pic_id in ids:
            GroupPictureDao.save_data(group_id,pic_id)

        return group_id


    # def save_data_insert(dic):
    #
    #     id = genUUID()
    #
    #     mysql = MysqlHelper()
    #
    #     _sql = "INSERT INTO news(`id`, "
    #     _val = " VALUES (%s,"
    #     _par = [id,]
    #
    #     for key in dic:
    #         _sql += "`"
    #         _sql += key
    #         _sql += "`,"
    #
    #         if type(dic[key]) == type(str):
    #             _val += "%s,"
    #         elif type(dic[key]) == type(int):
    #             _val += "%i,"
    #         else:
    #             _val += "%s,"
    #
    #         _par.append(dic[key])
    #
    #     _sql = _sql[0: len(_sql) - 1]
    #     _sql += ")"
    #
    #     _val = _val[0: len(_val) - 1]
    #     _val += ")"
    #
    #     _sql += _val
    #
    #     mysql.save(_sql, _par)
    #
    #     sql = "insert into "
    #     sql += article_table_name
    #     sql += " set id=%s"
    #     mysql.save(sql, id)


    def test(self):
        par = "content_url='0000',title='0000',type='0000'"

        self.save_data(par)


# tmp = PictureDao()
# tmp.save_data("http://baidu.com/a.jpg")


# test()


# PictureDao.save_group_data(['110','120','119','12306'])