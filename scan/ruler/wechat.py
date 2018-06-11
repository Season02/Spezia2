import time
import datetime

from ...scan.framework.json_scraper import ExtraJSON
# from ...scan.dao.scrapped_data_dao import ScrappdeDataDao
from ...scan.dao.picture_dao import PictureDao
from ...scan.dao.DBStructure import *

from CoTec.core.log.log_go import LogGo
from CoTec.utility.develop.tools import Annoations
from CoTec.core.request.request_go import RequestHelper
from CoTec.utility.string.string_go import *


class UrlHelper:
    @staticmethod
    def unify(url):
        url = StringHelper.unescape(url)
        res = url

        if url.count('chksm') >= 0:
            res = StringHelper.cutfrom(url, 'chksm')
            res += 'scene=0#wechat_redirec'

        return res

class WechatRuler:

    req = RequestHelper()
    """抓取关键字"""
    keys = ['author', 'content_url', 'cover', 'digest', 'title', 'datetime', 'fileid']

    """从 target 中获取 uuid 公众号 然后提取"""
    """返回结果为 dic 的 list ，每个 list 元素为一条微信"""

    @Annoations.exe_time
    def ExtraList(self, target, existsUrls, order):

        # order = ScrappdeDataDao.get_max_order_code()  # 数据库中排序代码
        result = []

        url = str(target.extra0)
        next_index = ""

        """抓取地址"""
        raw = WechatRuler.req._get(url)

        try:
            trup = ExtraJSON.extraWechatList(raw, 'msgList', WechatRuler.keys)
            list = trup[0]
            next_index = str(trup[1])
        except Exception as e:
            print(e)
            print("ERROR")
            return result

        while True:
            try:
                print('>>> scaning id: ' + next_index)
                LogGo.info('>>> scaning id: ' + next_index)
                tup = self.loopToFail(url, next_index)

                re_list = tup[0]
                next_index = str(tup[1])
                is_continue = tup[2]

                if len(re_list) > 0:
                    for item in re_list:
                        list.append(item)
                    # break
                else:
                    break

                if is_continue != 1:
                    break

            except Exception as e:
                print(e)
                break

        print('>>> list scaning completed')
        print('>>>')

        list.reverse()

        print('>>> Start Build SQL')
        result = self.build_base_dic(target,list,existsUrls,order)
        print('>>> Build SQL Success')
        print('>>>')

        return result

    def build_base_dic(self,target,list,existsUrls,order):
        news = TBNews()
        article = TBArticle()

        picture_dao = PictureDao()
        result = []
        article_result = []

        """抓取正文"""
        for i in list:
            try:
                i['content_url'] = UrlHelper.unify(i['content_url']) #StringHelper.unescape(i['content_url'])

                if existsUrls.count(i['content_url']) < 1:  # getattr(i, 'url')

                    LogGo.info(">>> file id: " + str(i['fileid']))
                    LogGo.info(">>> url: " + str(i['content_url']))

                    try:
                        tup = ExtraJSON.wechat_extra_content(i['content_url'])  # getattr(i, 'url')
                    except Exception as e:
                        print(e)
                        print(">>>  ")
                        print(">>> extra content error.")
                        print(">>>  ")
                        LogGo.info("extra content error.")
                        LogGo.info("possible a deleted msg")
                        # LogGo.info("url: " + i['content_url'])
                        continue

                    raw_content = tup[1]
                    content = tup[2]

                    """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
                    dic = dict()
                    article_dic = dict()

                    order = order + 5
                    dic[news.order_code.key] = order  # """排序代码"""
                    dic[news.create_date.key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # """此条记录创建时间"""
                    dic[news.valid.key] = 1
                    dic[news.text_not_format.key] = content #"""去除标签的正文内容"""
                    # dic[news.text_blob.key] = raw_content #"""原始带标签字段"""
                    dic[news.subscribe_time.key] = i['datetime']  # getattr(i, 'publicTime') """文章发表日期"""
                    dic[news.author.key] = i['author']  # getattr(i, 'author')"""文章所属机构"""
                    dic[news.title.key] = i['title']  # getattr(i, 'title')"""文章标题"""
                    dic[news.subject.key] = i['digest'] # """摘要"""
                    dic[news.status.key] = 2

                    picture_id = picture_dao.save_data(i['cover'])
                    dic[news.main_pic_id.key] = picture_id #"""列表图片 id"""

                    article_dic[article.fingerprint.key] = md5(i['content_url'])#"""由地址生成的指纹"""
                    article_dic[article.target_id.key] = target.id
                    article_dic[article.company.key] = target.data_key  # getattr(i, 'author') """文章所属机构"""
                    article_dic[article.content_url.key] = i['content_url']  # getattr(i, 'url')"""正文链接"""
                    article_dic[article.scrabble_type.key] = 'wechat'  # """文章类型 微信固定值为  wechat  """
                    article_dic[article.is_scrabbled.key] = 1  # """在数据库中作为 这是一条抓取到的数据 的标记"""

                    result.append(dic)
                    article_result.append(article_dic)
            except Exception as e:
                import traceback
                msg = traceback.format_exc()
                print(msg)
                LogGo.warning(repr(e))
                continue

        return result, article_result

    """生成 getmasssendmsg js 请求链接,并且进行请求操作，直到失败"""
    def loopToFail(self,url,index):

        "拆分请求url 提取参数 用在之后的请求中 """
        we_par_header = url.split('?')[0]
        we_par = url.split('?')[1]
        we_pars = we_par.split('&')

        we_pars_dic = dict()

        we_pars_dic['count'] = 10
        we_pars_dic['f'] = 'json'
        we_pars_dic['x5'] = 0

        we_pars_dic['frommsgid'] = str(index)
        we_pars_dic['wxtoken'] = ''

        for par in we_pars:
            tmp = par.split('=',1)
            we_pars_dic[tmp[0]] = tmp[1]

        request_url = ""
        request_url += we_par_header
        request_url += "?"

        dest = ['__biz','uin','key','f', 'frommsgid','count','uin','key','pass_ticket', 'wxtoken','x5']

        for key in dest:
            request_url += key
            request_url += "="
            request_url += str(we_pars_dic[key])
            request_url += "&"

        """抓取关键字"""
        # keys = ['author', 'content_url', 'cover', 'digest', 'title', 'datetime', 'fileid']
        """抓取地址"""
        # raw = RequestHelper.get(request_url)
        raw = WechatRuler.req._get(request_url)
        # print(raw)

        """ 采集数据 开始字符 采集关键字 """
        tup = ExtraJSON.extraGetMassList(raw, WechatRuler.keys)

        return tup

# wechat = 'http://mp.weixin.qq.com/s?__biz=MzI3NTE2NTQyNw==&mid=2650732480&idx=4&sn=7d80d2d219c2e7a99555e28ef5d88ef3&chksm=f302ae5cc475274a6034b1674a20a119e2e136f3076f4472443f0e6e30ded5944af416832433&scene=27#wechat_redirect'
# UrlHelper.unify(wechat)