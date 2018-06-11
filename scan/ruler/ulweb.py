import datetime
import random

from CoTec.core.exception.exception_go import *
from CoTec.core.exception.exception_go import ExceptionGo
from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_class_ver import RequestHelperClassVer
from CoTec.utility.date.date_go import DateGo
from CoTec.utility.develop.tools import Annoations
from CoTec.utility.string.string_go import *
from CoTec.utility.string.string_go import StringHelper as Sh
from CoTec.utility.download.dl import Download

from .BaseRuler import BaseRuler

from ...scan.dao.DBStructure import *
from ...scan.dao.picture_dao import PictureDao
from ...scan.framework.html_scraper import ExtraHtml
from ...scan.framework.json_scraper import ExtraJSON
from ...scan.framework.page_analyser import Analyser

from Spezia2.config.global_var import Configs


class UlWebRuler(BaseRuler):
    req = RequestHelperClassVer()
    extractor = ExtraHtml()

    def scan_list(self, target, exists) -> ():
        # order = ScrappdeDataDao.get_max_order('web')  # 数据库中排序代码

        detail_page_bundle_list = []

        error_code = None

        first = target.extra0#'http://ent.people.com.cn/GB/81374/index1.html'
        second = target.extra1#'http://ent.people.com.cn/GB/81374/index2.html'
        third = target.extra2#'http://ent.people.com.cn/GB/81374/index3.html'

        str_parent_container = target.extra3#'(div,[class:ej_list_box clear])'
        str_list_container = target.extra4#'(li,[])'
        list_ruler = target.extra5#'link:a href()=;title:a;data:em'
        content_ruler = target.extra6

        list_json_path = target.extra9

        url = ''

        one = False

        if second == "" or second is None:
            one = True
            url = first

        analyser = None
        if one == False:
            analyser = Analyser(first, second, third)

        try:
            encode = self.extractor.get_page_encode(first)
        except HttpConnectionFailedException as e:
            return (-2, (target, None, None, None))

        for i in range(1, Configs.length_web):
            LogGo.info('scaning index: ' + str(i))

            if one:
                pass
            else:
                url = analyser.get_url(i)
            try:
                raw = self.req.get(url,encode=encode)

                if target.type == 'ulweb':
                    self.looper_html(detail_page_bundle_list, raw, exists, list_ruler, str_parent_container, str_list_container)
                elif target.type == 'jsweb':
                    raw = self.extra4_process(target.extra4, raw)

                    self.looper_js(detail_page_bundle_list, raw, exists, list_ruler, str_parent_container, list_json_path=list_json_path)
                if one:
                    break
            except AttributeError as e:
                pass
            except TypeError as e:
                import traceback
                LogGo.warning(repr(e))
            except HttpConnectionFailedException as e:
                import traceback
                LogGo.warning(repr(e))
            except Exception as e:
                import traceback
                LogGo.warning(repr(e))

        if len(detail_page_bundle_list) > 0:
            detail_page_bundle_list.reverse()
            detail_page_bundle_list = self.purify(detail_page_bundle_list,'link')

            return (1, (target, detail_page_bundle_list, content_ruler, encode))
        else:
            return (-1, (target, None, None, None))

    def scan_detail(self, target, detail_page_bundle, order, content_ruler, encode):
        if detail_page_bundle is not None:
            return self.build_single_page_dic(target, detail_page_bundle, order, content_ruler, encode)
        else:
            return None

    def extra4_process(self, extra4, raw):
        """
        大概是处理字符编码的问题
        :param extra4:
        :param raw:
        :return:
        """
        res = raw

        if extra4 is not None and extra4 != '':
            parts = extra4.split(' ')

            if 'decode' in parts:
                res = raw.encode('latin-1').decode('unicode_escape')

        return res

    def container_process(self, raw:str, tribleStar:str) -> str:
        """
        前后剪裁
        :param extra4:
        :param raw:
        :return:
        """
        res = raw

        if tribleStar is not None and tribleStar != '':
            parts = tribleStar.split('***')

            res = Sh.strip_head_tail(raw, parts[0], parts[1])

        return res

    """
         疑似：解析 页面 ruler 转换内容

         extra3_tup: parent_container attribute 包含容器
         extra4_tup: list attribute 列表元素规则

         extra5: ruler 具体的元素提取规则

         注意： ruler 中必须有 link 元素!!!!!!!!!!!!
     """

    def looper_html_ex(self, result, raw, ruler, extra3_tup, extra4_tup):
        tup = Sh.str_to_dictup(extra3_tup)
        tag = tup[0]
        dic = tup[1]
        parent_container = (tag, dic)

        tup = Sh.str_to_dictup(extra4_tup)
        tag = tup[0]
        dic = tup[1]
        list_tup = (tag, dic)

        # 获取 list 提取成 字典
        list = ExtraHtml.any_list_finder_ex(raw, parent_container, list_tup)

        for item in list:
            if len(item) < 1:
                continue

            dic_list = ExtraHtml.tag_list_to_ruler_list_ex(item, ruler)

            result.append(dic_list)

    """
        疑似：获取新闻列表

        extra3_tup: parent_container attribute 包含容器
        extra4_tup: list attribute 列表元素规则

        extra5: ruler 具体的元素提取规则

        注意： ruler 中必须有 link 元素!!!!!!!!!!!!
    """
    def looper_html(self, result, raw, exists, ruler, extra3_tup, extra4_tup):
        tup = Sh.str_to_dictup(extra3_tup)
        tag = tup[0]
        dic = tup[1]
        parent_container = (tag, dic)

        tup = Sh.str_to_dictup(extra4_tup)
        tag = tup[0]
        dic = tup[1]
        list_tup = (tag, dic)

        # 获取 list 提取成 字典
        list = ExtraHtml.any_list_finder_ex(raw, parent_container, list_tup)

        for item in list:
            if len(item) < 1:
                continue

            dic_list = ExtraHtml.tag_list_to_ruler_list_ex(item, ruler)

            """日常抓取时的重复验证"""
            try:
                link = dic_list['link']
            except:
                break

            if exists.count(link) < 1:
                result.append(dic_list)
            else:
                break

    """
        extra3_tup: cap tup

        extra5: ruler
    """
    def looper_js(self, result:list, raw:str, exists:list, ruler:str, extra3_tup:str=None, list_json_path:str=None, identifier_key:str=None):
        # cap = ('data_callback(', ')')
        cap = None
        path = None

        if identifier_key is None:
            identifier_key = 'link'

        if extra3_tup is not None:
            cap = Sh.str_to_tup(extra3_tup)
        elif list_json_path is not None:
            path = Sh.separator(list_json_path, '->')

        list = ExtraJSON.extra_any_json(raw, ruler, cap=cap, list_path=path)

        if len(list) > 0:
            for item in list:
                """日常抓取时的重复验证"""
                if exists.count(item[identifier_key]) < 1:
                    result.append(item)
                else:
                    break

    def build_single_page_dic(self, target, detail_page_bundle, order, content_ruler, encode):
        picture_dao = PictureDao()
        news = TBNews()
        article = TBArticle()
        heavy = TBHeavyText()

        # news_result = []
        # article_result = []
        # heavy_result = []

        result_dic = {}

        i = detail_page_bundle

        index = 0
        """抓取正文"""
        try:
            link = str(i['link'])

            title = ''
            if Configs.show_utf:
                try:
                    title = i['title']
                except:
                    title = '<<error>>'

            LogGo.info(">>> index: " + str(index) + " " + title + "(" + link + ")")

            detail_page_supplement_bundle = dict()

            try:
                detail_page_supplement_bundle = self.extractor.web_extra_content(i['link'], content_ruler, encode)
            except HttpConnectionFailedException as e:
                LogGo.warning(repr(e))
                return (-3, None)
            except Exception as e:
                ExceptionGo.out_err(e)
                # print(str(e))
                # print(">>> extra content error.")
                LogGo.warning("extra content error." + '\r\r' + str(e))
                return (-2, None)

            item = i.copy()
            item.update(detail_page_supplement_bundle)

            # raw_content = tup[1]
            # content = tup[2]

            """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
            news_dic = dict()
            article_dic = dict()
            heavy_dic = dict()

            try:
                heavy_dic[heavy.text_not_format.key] = item['content'] # """去除标签的正文内容"""
                heavy_dic[heavy.text_blob.key] = item['content']
                # dic['text_blob'] = raw_content # """原始带标签字段"""

                news_dic[news.subscribe_time.key] = DateGo.trimDate(item['date'])  # """文章发表日期""" getattr
                news_dic[news.title.key] = item['title']  # getattr(i, 'title')
                article_dic[article.content_url.key] = item['link']  # """正文链接""" getattr(i, 'url')
            except KeyError as e:
                raise BaseDateLackException("No title! ")

            # try:
            #     dic[news.subscribe_time.key] = DateGo.trimDate(item['date'])  # """文章发表日期""" getattr
            # except:
            #     pass

            try:
                """文章作者"""
                news_dic[news.author.key] = item['author']  # getattr(i, 'author')
            except:
                pass

                news_dic[news.status.key] = 1
            order += 3
            news_dic[news.order_code.key] = order  # """排序代码"""
            news_dic[news.create_date.key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # """此条记录创建时间"""
            news_dic[news.valid.key] = 1

            article_dic[article.scrabble_type.key] = 'web' #"""文章类型"""
            article_dic[article.company.key] = target.data_key  # getattr(i, 'author') """文章所属机构"""
            article_dic[article.is_scrabbled.key] = 1#"""在数据库中作为 这是一条抓取到的数据 的标记"""
            article_dic[article.fingerprint.key] = md5(item['link'])  # """由地址生成的指纹"""
            article_dic[article.target_id.key] = target.id

            article_dic[article.publishStatus.key] = 1
            article_dic[article.messageType.key] = random.randint(0,1)

            """文章标签"""
            # try:
            #     dic['label'] = item['label']
            # except:
            #     pass

            try:
                """列表图片 id"""
                # path = Download.img(item['img'])
                # picture_id = picture_dao.save_data(path)
                # dic[news.main_pic_id.key] = picture_id
            except:
                pass

            result_dic.update(news_dic)
            result_dic.update(article_dic)
            result_dic.update(heavy_dic)
        except BaseDateLackException as e:
            msg = "Lake important data(" + str(e) + ')'
            LogGo.warning(msg)

            return (-1, None)
        except DataFormatException as e:
            msg = "Date format error: " + i['link'] + '\r\n' + str(e)
            LogGo.warning(msg)

            return (-1, None)
        except KeyError as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

            return (-1, None)
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

            return (-1, None)

        return (1, result_dic)

    # def build_base_dic(self, target, list, order, content_ruler, encode):
    #     picture_dao = PictureDao()
    #     news = TBNews()
    #     article = TBArticle()
    #     heavy = TBHeavyText()
    #
    #     news_result = []
    #     article_result = []
    #     heavy_result = []
    #
    #     index = 0
    #     """抓取正文"""
    #     for i in list:
    #         index += 1
    #         try:
    #             link = str(i['link'])
    #
    #             title = ''
    #             if Configs.show_utf:
    #                 try:
    #                     title = i['title']
    #                 except:
    #                     title = '<<error>>'
    #
    #             LogGo.info(">>> index: " + str(index) + " " + title + "(" + link + ")")
    #
    #             content = dict()
    #
    #             try:
    #                 content = self.extractor.web_extra_content(i['link'], content_ruler, encode)
    #             except Exception as e:
    #                 ExceptionGo.out_err(e)
    #                 # print(str(e))
    #                 # print(">>> extra content error.")
    #                 LogGo.warning("extra content error." + '\r\r' + str(e))
    #                 continue
    #
    #             item = i.copy()
    #             item.update(content)
    #
    #             # raw_content = tup[1]
    #             # content = tup[2]
    #
    #             """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
    #             dic = dict()
    #             article_dic = dict()
    #             heavy_dic = dict()
    #
    #             try:
    #                 heavy_dic[heavy.text_not_format.key] = item['content'] # """去除标签的正文内容"""
    #                 # dic['text_blob'] = raw_content # """原始带标签字段"""
    #
    #                 dic[news.subscribe_time.key] = DateGo.trimDate(item['date'])  # """文章发表日期""" getattr
    #                 dic[news.title.key] = item['title']  # getattr(i, 'title')
    #                 article_dic[article.content_url.key] = item['link']  # """正文链接""" getattr(i, 'url')
    #             except KeyError as e:
    #                 raise BaseDateLackException(str(e))
    #
    #             # try:
    #             #     dic[news.subscribe_time.key] = DateGo.trimDate(item['date'])  # """文章发表日期""" getattr
    #             # except:
    #             #     pass
    #
    #             try:
    #                 """文章作者"""
    #                 dic[news.author.key] = item['author']  # getattr(i, 'author')
    #             except:
    #                 pass
    #
    #             dic[news.status.key] = 1
    #             order += 3
    #             dic[news.order_code.key] = order  # """排序代码"""
    #             dic[news.create_date.key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # """此条记录创建时间"""
    #             dic[news.valid.key] = 1
    #
    #             article_dic[article.scrabble_type.key] = 'web' #"""文章类型"""
    #             article_dic[article.company.key] = target.data_key  # getattr(i, 'author') """文章所属机构"""
    #             article_dic[article.is_scrabbled.key] = 1#"""在数据库中作为 这是一条抓取到的数据 的标记"""
    #             article_dic[article.fingerprint.key] = md5(item['link'])  # """由地址生成的指纹"""
    #             article_dic[article.target_id.key] = target.id
    #
    #             """文章标签"""
    #             # try:
    #             #     dic['label'] = item['label']
    #             # except:
    #             #     pass
    #
    #             try:
    #                 """列表图片 id"""
    #                 # path = Download.img(item['img'])
    #                 # picture_id = picture_dao.save_data(path)
    #                 # dic[news.main_pic_id.key] = picture_id
    #             except:
    #                 pass
    #
    #             news_result.append(dic)
    #             article_result.append(article_dic)
    #             heavy_result.append(heavy_dic)
    #         except BaseDateLackException as e:
    #             msg = "Lake important data(" + str(e) + ')'
    #             # print(msg)
    #             LogGo.warning(msg)
    #         except DataFormatException as e:
    #             msg = "Date format error: " + i['link'] + '\r\n' + str(e)
    #             # print(msg)
    #             LogGo.warning(msg)
    #             continue
    #         except KeyError as e:
    #             import traceback
    #             msg = traceback.format_exc()
    #             # print(msg)
    #             LogGo.warning(msg)
    #             continue
    #         except Exception as e:
    #             import traceback
    #             msg = traceback.format_exc()
    #             # print(msg)
    #             LogGo.warning(msg)
    #             continue
    #
    #     return news_result, article_result, heavy_result

    """去重"""
    # @Annoations.exe_time
    def purify(self, list, key):
        if len(list) < 1:
            return

        result = []
        index = 0

        for i in list:
            flag = True
            id = i[key]

            for seq in result[::-1]:
                sid = seq[key]
                if id == sid:
                    flag = False
                    break

            if flag:
                result.append(i)

        return result

