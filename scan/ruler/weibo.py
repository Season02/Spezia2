import time

from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_go import RequestHelper
from CoTec.utility.date.date_go import DateGo
from CoTec.utility.develop.tools import Annoations

from ...scan.dao.DBStructure import *
# from ...scan.dao.scrapped_data_dao import ScrappdeDataDao
from ...scan.framework.json_scraper import ExtraJSON

from .BaseRuler import BaseRuler

from Spezia2.config.global_var import Configs

"""
微博有提供用来获取信息列表的的 API 但api的使用有一些很不方便的限制，所以采用抓取的策略
微博网站上的规则是比较复杂的，不容易下手，反观 weibo.cn 这个移动端的网站，内容简单许多

主要思路 模拟登陆，在微博服务器有 session 记录，然后使用 js 来获取微博
主要参考资料 https://segmentfault.com/a/1190000000498692
"""
class WeiboRuler(BaseRuler):
    req = RequestHelper()

    request_login = 'https://passport.weibo.cn/sso/login'
    url_login = "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F%2F%3Fjumpfrom%3Dwapv4%26tip%3D1%26vt%3D4"
    # request_getindex = 'http://m.weibo.cn/container/getIndex'
    request_getindex = 'https://m.weibo.cn/api/container/getIndex'
    url_status = 'http://m.weibo.cn/status/'

    limited_attitude_count = 0
    limited_forward_count = 0

    exist_program = []

    """请求参数"""
    par = (['username', Configs.weibo_username], ['password', Configs.weibo_password],
           ['savestate', 1], ['ec', 0], ['entry', 'mweibo'])
    """抓取关键字"""
    keys = ['title', 'author', 'publicTime', 'url', 'clicksCount', 'likeCount', 'publicTime']
    """请求"""
    header = \
        {
            "User-Agent":
                "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Mobile Safari/537.36",
            "Referer":
                "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F%3Fjumpfrom%3Dwapv4%26tip%3D1",
            "Origin":
                "https://passport.weibo.cn",
            "Host":
                "passport.weibo.cn",
            "DNT":
                "1",
            "Content-Type":
                "application/x-www-form-urlencoded",
            "Connection":
                "keep-alive",
            "Accept-Language":
                "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "Accept-Encoding":
                "gzip, deflate, br",
        }

    def scan_list(self, target, exists):
        self.limited_forward_count = target.limited_forward_count
        self.limited_attitude_count = target.limited_attitude_count

        list = []
        result_list = []

        """模拟登陆"""
        status = 'you got it'

        """如果登陆成功"""
        if status != '':
            self.loops(target,exists,list)
            if len(list) < 1:
                return (0, (target, None, None, None))
        else:
            LogGo.warning("Weibo: Loop scan faild!")
            return (-1, (target, None, None, None))

        if len(list) > 0:
            list = self.purify(list)
            list.reverse()

            for item in list:
                if exists.count(item['id']) < 1:
                    result_list.append(item)

            LogGo.debug('newrank list length:' + str(len(result_list)))

        if len(result_list) > 0:
            return (1, (target, list, None, None))
        return(-1, (target, None, None, None))

    def scan_detail(self, target, detail_page_bundle, order, content_ruler, encode):
        self.limited_forward_count = target.limited_forward_count
        self.limited_attitude_count = target.limited_attitude_count

        if detail_page_bundle is not None:
            return self.build_single_page_dic(target, detail_page_bundle, order, content_ruler, encode)
        else:
            return None

    """获取最新的微博"""
    # def scan_latest(self, target, exists, order):
    #     # order = ScrappdeDataDao.get_max_order('weibo')  # 数据库中排序代码
    #
    #     result = []
    #
    #     """模拟登陆"""
    #     status = WeiboRuler.req._get(WeiboRuler.url_login)
    #     raw = WeiboRuler.req.post_ex(WeiboRuler.request_login, WeiboRuler.par, header=WeiboRuler.header)
    #
    #     """如果登陆成功"""
    #     if status != '':
    #         base_url = target.extra0
    #         for i in range(1, Configs().length_weibo):
    #             print("page: " + str(i))
    #
    #             list = self.build_and_request(WeiboRuler.keys, base_url, WeiboRuler.request_getindex, i)
    #
    #             if len(list) == 0:
    #                 break
    #             for item in list:
    #                 """日常抓取时的重复验证"""
    #                 if exists.count(item['id']) < 1:
    #                     result.append(item)
    #                 else:
    #                     break
    #     else:
    #         LogGo.warning("Weibo: Simulation Weibo Login Failed!")
    #         raise Exception("Invalid Username or Password")
    #
    #     list = self.build_base_dic(result, exists, order, target)
    #     return list

    # def scan(self,target,exists, order, exists_program:list):
    #     # order = ScrappdeDataDao.get_max_order('weibo')  # 数据库中排序代码
    #
    #     self.limited_forward_count = target.limited_forward_count
    #     self.limited_attitude_count = target.limited_attitude_count
    #
    #     self.exist_program = exists_program
    #
    #     result = []
    #
    #     """模拟登陆"""
    #     status = 'you got it'#WeiboRuler.req._get(WeiboRuler.url_login)
    #     # raw = WeiboRuler.req.post_ex(WeiboRuler.request_login, WeiboRuler.par,header=WeiboRuler.header)
    #
    #     """如果登陆成功"""
    #     if status != '':
    #         self.loops(target,exists,result)
    #         if len(result) < 1:
    #             return None
    #     else:
    #         LogGo.warning("Weibo: Simulation Weibo Login Failed!")
    #         raise Exception("Invalid Username or Password")
    #
    #     result = self.purify(result)
    #
    #     result.reverse()
    #
    #     return self.build_base_dic(result,exists,order, target)

    # @Annoations.exe_time
    def loops(self,target,exists,result):
        try:
            base_url = target.extra0
            for i in range(0, Configs().length_weibo):  # [::-1]:
                print("page: " + str(i))

                list = self.build_and_request(WeiboRuler.keys, base_url, WeiboRuler.request_getindex, i)

                if len(list) == 0:
                    break
                for item in list:
                    """日常抓取时的重复验证"""
                    if exists.count(item['id']) < 1:
                        result.append(item)
                    else:
                        return
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            print(msg)
            LogGo.warning(repr(e))
            LogGo.warning("Scan Failed!")
            return

    """
    根据 id 去除重复微博(抓取重复验证，因为微博的更新很快，有可能在抓取途中就发生了位移)
    从 index = 0 开始遍历,若不重复则 放入 result ，result 的重复检测设置个限制，就 100吧
    倒序查找我认为更有效率

    20180306:
    增加过滤条件：转发量（大于），点赞量（大于），节目数量检查（3个以下）
    """
    # @Annoations.exe_time
    def purify(self,list):
        if len(list) < 1:
            return []

        result = []

        for i in list:
            try:
                flag = True

                id = i['id']
                text = i['text']

                limited_attitude_count = i['attitudes_count']
                limited_forward_count = i['reposts_count']

                program_count = 0

                # 基础过滤重复id
                for seq in result[::-1]:
                    sid = seq['id']
                    if id == sid:
                        flag = False
                        break

                # 第一次节目名过滤（有可能会包含到非节目）
                if flag and text.count('《') < 1:
                    flag = False

                # 条二次参数过滤
                if flag and self.limited_attitude_count is not None and limited_attitude_count is not None:
                    if limited_attitude_count < self.limited_attitude_count:
                        flag = False

                if flag and self.limited_forward_count is not None and limited_forward_count is not None:
                    if limited_forward_count < self.limited_forward_count:
                        flag = False

                # 第三次依据节目名过滤
                if flag:
                    for program in self.exist_program:
                        if text.count(program) >= 1:
                            program_count = program_count + 1

                        if program_count > 3:
                            flag = False
                            break

                if flag:
                    result.append(i)
            except Exception as e:
                import traceback
                msg = traceback.format_exc()
                LogGo.warning(msg)

        return result

    def build_single_page_dic(self, target, detail_page_bundle, order, content_ruler, encode):
        news = TBNews()
        article = TBArticle()

        result_dic = dict()

        try:
            LogGo.info(WeiboRuler.url_status + detail_page_bundle['id'])

            # blob = i['text'].encode("UTF-8")

            """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
            news_dic = dict()
            article_dic = dict()

            """排序代码"""
            order += 2
            news_dic[news.order_code.key] = order
            # dic[news.text_not_format.key] = i['text']#"""去除标签的正文内容"""
            # dic[news.text_blob.key] = blob #"""原始带标签字段"""

            sub_tim = detail_page_bundle['created_at']
            if sub_tim is not None:
                news_dic[news.subscribe_time.key] = sub_tim  # getattr(i, 'publicTime') """文章发表日期"""
            else:
                LogGo.warning("no subscribe time!")

            news_dic[news.create_date.key] = DateGo.get_current_date()  # """此条记录创建时间"""
            news_dic[news.status.key] = 1  # """状态"""
            news_dic[news.valid.key] = 1

            news_dic[news.title.key] = detail_page_bundle['text']
            news_dic[news.text_not_format.key] = detail_page_bundle['text']
            news_dic[news.text_blob.key] = detail_page_bundle['text']

            # title = None
            # try:
            #     title = i['page_info']
            #     title = title['content1']
            # except Exception as e:
            #     pass

            # if title is None:
            #     dic[news.title.key] = i['text']  # getattr(i, 'title') """文章标题"""
            # else:
            #     dic[news.title.key] = title # """文章标题"""

            """文章所属机构"""
            try:
                user = detail_page_bundle['user']
                screen_name = user['screen_name']
                article_dic[article.company.key] = screen_name  # getattr
            except Exception as e:
                pass

            article_dic[article.vote_up_count.key] = detail_page_bundle['attitudes_count']  # getattr(i, 'likeCount') """点赞数"""
            article_dic[article.scrabble_type.key] = 'weibo' #"""文章类型"""
            article_dic[article.is_scrabbled.key] = 1 #"""在数据库中作为 这是一条抓取到的数据 的标记"""
            article_dic[article.identifier.key] = detail_page_bundle['id'] #"""数据在母体中的 id"""
            article_dic[article.target_id.key] = target.id
            article_dic[article.content_url.key] = WeiboRuler.url_status + detail_page_bundle['id']  # getattr(i, 'url') """正文链接"""

            article_dic[article.publishStatus.key] = 1
            # article_dic[article.messageType.key] = random.randint(0, 1)

            """如果是回复 或者 引用 会有被引用的微博，记录那个微博的 id"""
            try:
                retweeted_status = detail_page_bundle['retweeted_status']
                ret_id = retweeted_status['id']

                article_dic[article.identifier_re.key] = ret_id
            except Exception as e:
                pass

            """阅读量"""
            # dic['click_count'] = i['clicksCount'] #getattr(i, 'clicksCount')
            """转发数"""
            """评论量"""

            # """图片组"""
            # try:
            #     pics = i['pics']
            #     if len(pics) > 0:
            #         group_id = PictureDao.save_group_data(pics)
            #         if group_id is not None:
            #             dic['group_picture_id'] = group_id
            # except Exception as e:
            #     print(e)
            #     LogGo.warning(dic['content_url'])
            #     LogGo.warning(e)

            result_dic.update(article_dic)
            result_dic.update(news_dic)
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

            return None

        return result_dic

    # def build_base_dic(self,result,exists,order, target):
    #     list = []
    #     a_list = []
    #
    #     news = TBNews()
    #     article = TBArticle()
    #
    #     for i in result:
    #         try:
    #             if exists.count(i['id']) < 1:  # getattr(i, 'url')
    #
    #                 LogGo.info(WeiboRuler.url_status + i['id'])
    #
    #                 # blob = i['text'].encode("UTF-8")
    #
    #                 """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
    #                 dic = dict()
    #                 article_dic = dict()
    #
    #                 """排序代码"""
    #                 order += 2
    #                 dic[news.order_code.key] = order
    #                 # dic[news.text_not_format.key] = i['text']#"""去除标签的正文内容"""
    #                 # dic[news.text_blob.key] = blob #"""原始带标签字段"""
    #
    #                 sub_tim = i['created_at']
    #                 if sub_tim is not None:
    #                     dic[news.subscribe_time.key] = sub_tim  # getattr(i, 'publicTime') """文章发表日期"""
    #                 else:
    #                     LogGo.warning("no subscribe time!")
    #
    #                 dic[news.create_date.key] = DateGo.get_current_date()  # """此条记录创建时间"""
    #                 dic[news.status.key] = 1  # """状态"""
    #                 dic[news.valid.key] = 1
    #
    #                 dic[news.title.key] = i['text']
    #
    #                 # title = None
    #                 # try:
    #                 #     title = i['page_info']
    #                 #     title = title['content1']
    #                 # except Exception as e:
    #                 #     pass
    #
    #                 # if title is None:
    #                 #     dic[news.title.key] = i['text']  # getattr(i, 'title') """文章标题"""
    #                 # else:
    #                 #     dic[news.title.key] = title # """文章标题"""
    #
    #                 """文章所属机构"""
    #                 try:
    #                     user = i['user']
    #                     screen_name = user['screen_name']
    #                     article_dic[article.company.key] = screen_name  # getattr
    #                 except Exception as e:
    #                     pass
    #
    #                 article_dic[article.vote_up_count.key] = i['attitudes_count']  # getattr(i, 'likeCount') """点赞数"""
    #                 article_dic[article.scrabble_type.key] = 'weibo' #"""文章类型"""
    #                 article_dic[article.is_scrabbled.key] = 1 #"""在数据库中作为 这是一条抓取到的数据 的标记"""
    #                 article_dic[article.identifier.key] = i['id'] #"""数据在母体中的 id"""
    #                 article_dic[article.target_id.key] = target.id
    #                 article_dic[article.content_url.key] = WeiboRuler.url_status + i['id']  # getattr(i, 'url') """正文链接"""
    #
    #                 """如果是回复 或者 引用 会有被引用的微博，记录那个微博的 id"""
    #                 try:
    #                     retweeted_status = i['retweeted_status']
    #                     ret_id = retweeted_status['id']
    #
    #                     article_dic[article.identifier_re.key] = ret_id
    #                 except Exception as e:
    #                     pass
    #
    #                 list.append(dic)
    #                 a_list.append(article_dic)
    #
    #                 """阅读量"""
    #                 # dic['click_count'] = i['clicksCount'] #getattr(i, 'clicksCount')
    #                 """转发数"""
    #                 """评论量"""
    #
    #                 # """图片组"""
    #                 # try:
    #                 #     pics = i['pics']
    #                 #     if len(pics) > 0:
    #                 #         group_id = PictureDao.save_group_data(pics)
    #                 #         if group_id is not None:
    #                 #             dic['group_picture_id'] = group_id
    #                 # except Exception as e:
    #                 #     print(e)
    #                 #     LogGo.warning(dic['content_url'])
    #                 #     LogGo.warning(e)
    #
    #         except Exception as e:
    #             import traceback
    #             msg = traceback.format_exc()
    #             LogGo.warning(msg)
    #             # LogGo.warning(WeiboRuler.url_status + i['id'])
    #
    #     return list, a_list

    """
    通过给定的 首页 url 拼接出分页请求用地址，并且发出请求获得回应数据
    """
    def build_and_request(self, keys, base_url, url, page):

        we_par_header = base_url.split('?')[0]
        we_par = base_url.split('?')[1]
        we_pars = we_par.split('&')

        _we_pars = dict()

        for par in we_pars:
            tmp = par.split('=',1)
            _we_pars[tmp[0]] = tmp[1]

        we_pars_dic = dict()

        we_pars_dic['uid'] = _we_pars['uid']
        we_pars_dic['luicode'] = _we_pars['luicode']
        we_pars_dic['type'] = 'uid'
        we_pars_dic['value'] = _we_pars['uid']
        we_pars_dic['lfid'] = _we_pars['lfid']
        we_pars_dic['containerid'] = '107603' + _we_pars['uid']

        # we_pars_dic['featurecode'] = '0'
        # we_pars_dic['retcode'] = '0'

        request_url = ""
        request_url += url
        request_url += "?"

        """dest 标注参数拼接的顺序"""
        dest = ['uid', 'luicode', 'lfid', 'type', 'value', 'containerid']
        # dest = ['uid', 'luicode', 'lfid', 'featurecode', 'retcode', 'type', 'value', 'containerid']

        for key in dest:
            request_url += key
            request_url += "="
            request_url += str(we_pars_dic[key])
            request_url += "&"

        if int(page) > 1:
            request_url += 'page=' + str(page)

        """抓取地址"""
        # raw = RequestHelper.get(request_url)
        raw = WeiboRuler.req._get(request_url)
        # print(raw)

        """ 采集数据 开始字符 采集关键字 """
        tup = ExtraJSON.extra_getindex_list(raw, keys)

        return tup




# weibo = WeiboRuler()
#
# list = [{'id': '1',},{'id': '1',},{'id': '3',},{'id': '3',},{'id': '3',},{'id': '6',},{'id': '8',},{'id': '8',},]
# result = weibo.purify(list)
#
# print(result)