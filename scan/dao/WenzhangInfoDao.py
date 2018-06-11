from CoTec.core.database.GeneralDao import GeneralDao
from .DBStructure import *

from Spezia2.config.global_var import Configs


class WenzhangInfoDao(GeneralDao):
    def __init__(self):
        GeneralDao.__init__(self, Configs())

        self.TB = TBWenzhangInfo()
        self.table_name = self.TB.TableName

    # def get_all_wenzhang(self):
    #     select_list = [TBNews.id,'click_count','create_time','order_code','status','subcribe_time','text_not_format_clob','company','content_url','scrap_type','title']
    #
    #     val = self.get_list(self.table_name,select_list)
    #     return val

    def get(self,select_list,where=None,limit=None,order=None,group=None):
        val = self.get_list(self.table_name, select_list=select_list, where_dic=where, limit_tup=limit, order_tup=order, group_str=group)

        if len(select_list) == 1:
            result = []
            for item in val:
                result.append(item[select_list[0]])
            return result

        return val

    def update(self, update, where):
        sta = self.update_with_dic(self.table_name, update, where)
        return sta


# wenzhang = WenzhangDaoInfo()
# TB = TBWenzhangInfo()
# select = [TB.title.key,TB.description.key,TB.wx_hao.key,TB.date_time.key]
#
#
# res = wenzhang.get(select_list=select)
# print(res)