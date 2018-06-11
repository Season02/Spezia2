import datetime
import time

from ...scan.framework.json_scraper import ExtraJSON
# from ...scan.dao.scrapped_data_dao import ScrappdeDataDao
from ...scan.dao.picture_dao import PictureDao
from ...scan.dao.DBStructure import *
from CoTec.core.exception.exception_go import *
from ...config.global_var import Configs

from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_go import RequestHelper
from CoTec.core.exception.exception_go import ExceptionGo as E
from CoTec.utility.string.string_go import StringHelper as Sh
from CoTec.utility.develop.tools import Annoations
from CoTec.utility.string.string_go import *
from CoTec.utility.date.date_go import DateGo

from ..dao.news_dao import NewsDao

from .BaseRuler import BaseRuler

class Entity:
    def __init__(self, name, publicId, uuid):
        self.name = name
        self.publicId = publicId
        self.uuid = uuid

class GsdataRuler(BaseRuler):

    jsons = ExtraJSON()

    req = RequestHelper()
    url = 'http://www.gsdata.cn/rank/toparc?wxname={0}&wx={1}&sort=-1'

    def __init__(self):
        self.news = NewsDao()

    """从 target 中获取 uuid 公众号 然后提取"""
    """返回结果为 dic 的 list ，每个 lfist 元素为一条微信"""
    def looper_js(self, result, raw, exists, ruler, captup=None):
        cap = captup
        if captup != None:
            if captup.count(' ') == 2:
                cap = Sh.str_to_tup(captup)

        list = ExtraJSON.extra_any_json(raw, ruler, cap=cap)

        if len(list) > 0:
            for item in list:
                """日常抓取时的重复验证"""
                if 1>0:#if exists.count(item['link']) < 1:
                    result.append(item)
                else:
                    break

    def sort(self, list):
        for i in range(0,len(list)):
            for j in range(i + 1, len(list)):
               if list[i]['date'] < list[j]['date'] or list[i]['date'] == list[j]['date'] and list[i]['top'] > list[j]['top'] :
                   list[i], list[j] = list[j], list[i]

        return list

    def scan_list(self, target, exists):
        list = []
        result_list = []

        cap = 'data'

        ruler = 'author:author;title:title;date:posttime;img:picurl;link:url;top:top;click:readnum_newest;vote_up:likenum_newest;subject:content'

        url = self.url.format(target.extra0, target.wx_hao)
        header = {'X-Requested-With': 'XMLHttpRequest'}

        raw = RequestHelper.get(url, header=header, file_cookie=Configs.gsdata_cookie_file)

        try:
            self.looper_js(list, raw, exists, ruler, cap)
        except Exception as e:
            E.out_err(e)
            return (-1, (target, None, None, None))

        if len(list) > 0:
            list = self.sort(list)
            list.reverse()

            for item in list:
                if exists.count(item['title']) < 1:
                    result_list.append(item)

            LogGo.debug('newrank list length:' + str(len(result_list)))

        if len(result_list) > 0:
            return (1, (target, list, None, None))
        return(-1, (target, None, None, None))

    def scan_detail(self, target, detail_page_bundle, order, content_ruler, encode):
        news = TBNews()
        article = TBArticle()

        # picture_dao = PictureDao()

        result_dic = dict()

        try:
            """由地址生成的指纹"""
            signature = md5(detail_page_bundle['link'])

            info = self.ready_info(detail_page_bundle['title'], detail_page_bundle['link'])
            LogGo.info(info)

            try:
                tup = self.jsons.wechat_extra_content(detail_page_bundle['link'])  # getattr(i, 'url')
            except HttpConnectionFailedException as e:
                LogGo.warning(repr(e))
                return (-3, None)
            except AttributeError as ae:
                LogGo.warning("Maybe a deleted msg, complete the code to detect this error")
                return (-2, None)

            raw_content = tup[1]
            content = tup[2]

            """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
            news_dic = dict()
            article_dic = dict()

            ############################## NEWS ###############################

            """列表图片"""
            picture = detail_page_bundle['img']
            """列表图片 id"""
            # if picture is not None:
            #     picture_id = picture_dao.save_data(picture)
            #     news_dic[news.main_pic_id.key] = picture_id

            order = order + 2
            news_dic[news.order_code.key] = order  # """排序代码"""
            news_dic[news.subject.key] = detail_page_bundle['subject']  # """摘要"""
            news_dic[news.valid.key] = 1
            news_dic[news.create_date.key] = datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')  # """此条记录创建时间"""
            news_dic[news.text_not_format.key] = content  # """去除标签的正文内容"""
            # news_dic[news.text_blob.key] = raw_content #"""原始带标签字段"""
            news_dic[news.title.key] = detail_page_bundle['title']  # getattr(i, 'title') """文章标题"""
            news_dic[news.subscribe_time.key] = detail_page_bundle['date']  # getattr(i, 'publicTime') """文章发表日期"""
            news_dic[news.status.key] = 2

            try:
                news_dic[news.author.key] = detail_page_bundle['author']  # getattr(i, 'clicksCount') """阅读量"""
            except:
                pass

            ############################## ARTICLE ###############################

            try:
                article_dic[article.raw_click_count.key] = int(
                    detail_page_bundle['click'])  # getattr(i, 'clicksCount') """阅读量"""
            except:
                pass

            try:
                article_dic[article.vote_up_count.key] = int(
                    detail_page_bundle['vote_up'])  # getattr(i, 'likeCount') """点赞数"""
            except:
                pass

            article_dic[article.scrabble_type.key] = 'wechat'  # """文章类型 微信固定值为  wechat  """
            article_dic[article.is_scrabbled.key] = 1  # """在数据库中作为 这是一条抓取到的数据 的标记"""
            article_dic[article.fingerprint.key] = signature  # """由地址生成的指纹"""
            article_dic[article.target_id.key] = target.id
            article_dic[article.company.key] = target.data_key  # getattr(i, 'author') """文章所属机构"""
            article_dic[article.content_url.key] = detail_page_bundle['link']  # getattr(i, 'url') """正文链接"""

            article_dic[article.publishStatus.key] = 1
            # article_dic[article.messageType.key] = random.randint(0, 1)

            ############################## DIC ###############################

            result_dic.update(article_dic)
            result_dic.update(news_dic)
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

            return (-1, None)

        return (1, result_dic)
