from CoTec.core.database.mysql_go import MysqlHelper
from CoTec.utility.string.string_go import genUUID

from ...config.global_var import Configs

tableName = 'group_picture'


class GroupPictureDao:
    def save_data(group_id,picture_id):

        id = genUUID()

        dic = dict()
        dic['group_id'] = group_id
        dic['picture_id'] = picture_id

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



# tmp = PictureDao()
# tmp.save_data("http://baidu.com/a.jpg")
