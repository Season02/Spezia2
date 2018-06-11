import datetime

from ...scan.framework.json_scraper import ExtraJSON

from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_go import RequestHelper
from CoTec.utility.string.string_go import *

from ..dao.DBStructure import *
from CoTec.core.exception.exception_go import *
from .BaseRuler import BaseRuler

from ...config.global_var import Configs


class Entity:
    def __init__(self, name, publicId, uuid):
        self.name = name
        self.publicId = publicId
        self.uuid = uuid

class NewrankRuler(BaseRuler):
    jsons = ExtraJSON()

    req = RequestHelper()
    url = 'https://www.newrank.cn/xdnphb/detail/getAccountArticle'

    """从 target 中获取 uuid 公众号 然后提取"""
    """返回结果为 dic 的 list ，每个 list 元素为一条微信"""

    def scan_list(self, target, exists):
        """请求参数"""
        par = (['flag', 'true'], ['uuid', target.extra0])
        """抓取关键字"""
        keys = ['title', 'author', 'publicTime', 'url', 'clicksCount', 'likeCount', 'publicTime', 'summary']

        list = []
        result_list = []

        try:
            raw = RequestHelper.post(NewrankRuler.url, par, file_cookie=Configs.newrank_cookie_file)
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            # print(msg)
            LogGo.warning(msg)
            return (-1, (target, None, None, None))

        try:
            list = ExtraJSON.extra_newrank_wechat_list(raw,keys)
        except:
            return (-1, (target, None, None, None))

        if len(list) > 0:
            list.reverse()

            for item in list:
                if exists.count(item['title']) < 1:
                    result_list.append(item)

            LogGo.debug('newrank list length:' + str(len(result_list)))

        if len(result_list) > 0:
            return (1, (target, list, None, None))
        return(-1, (target, None, None, None))

    # def test_loop(self, ):

    def scan_detail(self, target, detail_page_bundle, order, content_ruler, encode):
        news = TBNews()
        article = TBArticle()

        # picture_dao = PictureDao()

        result_dic = dict()

        try:
            info = self.ready_info(detail_page_bundle['title'], detail_page_bundle['url'])
            LogGo.info(info)

            try:
                # tup = ExtraJSON.wechat_extra_content(detail_page_bundle['url'])
                tup = self.jsons.wechat_extra_content(detail_page_bundle['url'])
            except HttpConnectionFailedException as e:
                LogGo.warning(repr(e))
                return (-3, None)
            except AttributeError:
                LogGo.warning("Maybe a deleted msg, complete the code to detect this error")
                return (-2, None)
            except Exception:
                LogGo.warning("Error when get detail message!")
                return (-2, None)

            raw_content = tup[1]
            content = tup[2]
            picture = tup[3]

            """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
            news_dic = dict()
            article_dic = dict()

            ############################## NEWS ###############################

            """列表图片 id"""
            # if picture is not None:
            #     picture_id = picture_dao.save_data(picture)
            #     news_dic[news.main_pic_id.key] = picture_id

            news_dic[news.text_not_format.key] = content  # """去除标签的正文内容"""
            # dic[news.text_blob.key] = raw_content#"""原始带标签字段"""
            news_dic[news.subscribe_time.key] = detail_page_bundle['publicTime']  # """文章发表日期"""
            news_dic[news.create_date.key] = datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S')  # """此条记录创建时间"""
            news_dic[news.subject.key] = detail_page_bundle['summary']  # """摘要"""
            news_dic[news.valid.key] = 1
            news_dic[news.author.key] = detail_page_bundle['author']
            news_dic[news.title.key] = detail_page_bundle['title']  # """文章标题"""
            news_dic[news.status.key] = 2
            order += 5
            news_dic[news.order_code.key] = order  # """排序代码"""

            ############################## ARTICLE ###############################

            article_dic[article.content_url.key] = detail_page_bundle['url']  # getattr(i, 'url')"""正文链接"""
            article_dic[article.fingerprint.key] = md5(detail_page_bundle['url'])  # """由地址生成的指纹"""
            article_dic[article.company.key] = target.data_key  # """文章所属机构"""
            article_dic[article.target_id.key] = target.id
            article_dic[article.raw_click_count.key] = detail_page_bundle['clicksCount']  # getattr(i, 'clicksCount')#"""阅读量"""
            article_dic[article.vote_up_count.key] = detail_page_bundle['likeCount']  # getattr(i, 'likeCount')"""点赞数"""
            article_dic[article.scrabble_type.key] = 'wechat'  # """文章类型 微信固定值为  wechat  """
            article_dic[article.is_scrabbled.key] = 1  # """在数据库中作为 这是一条抓取到的数据 的标记"""

            article_dic[article.publishStatus.key] = 1
            # article_dic[article.messageType.key] = random.randint(0, 1)

            ############################## DIC ###############################

            result_dic.update(news_dic)
            result_dic.update(article_dic)
        except Exception:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

            return (-1, None)

        return (1, result_dic)

