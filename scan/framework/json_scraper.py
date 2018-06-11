import demjson
import time
import datetime

from bs4 import BeautifulSoup
from bs4.element import Tag

from ...scan.framework.html_scraper import ExtraHtml

from CoTec.core.log.log_go import LogGo
# from CoTec.core.request.request_go import RequestHelper
from CoTec.core.request.request_class_ver import RequestHelperClassVer

from CoTec.utility.date.date_go import DateGo
from CoTec.utility.string.string_go import StringHelper

class ExtraJSON:
    """微信正文内容抓取函数，正式中会尽量根据数据库动态调整"""
    req = RequestHelperClassVer()

    """返回结果为 元组"""
    # @staticmethod
    def wechat_extra_content(self, url):

        # raw = RequestHelper.get(url)
        raw = self.req.get(url)

        soup = BeautifulSoup(raw, "html.parser")
        title = soup.title.text

        pictures = soup.find_all("img", {"data-type": {"jpeg", "png", "gif"}})
        picture = None
        if len(pictures) > 2:
            picture = soup.find("img", {"data-type": {"jpeg", "png", "gif"}}).attrs['data-src']

        # author = soup.find("div", {"class": "rich_media_meta_list"}).children

        tags = soup.find("div", {"class": "rich_media_content", "id": "js_content"}).findAll({"p"})

        if len(tags) < 3:
            tags = soup.find("div", {"class": "rich_media_content", "id": "js_content"}).findAll({"section"})

        # content = ""
        raw = ''
        not_format = ''

        """如果第一或第二个标签是 <p><br/></p> 形式的 删除第一或个标签"""
        escape_list = [False, False]

        if len(tags[0].contents) == 1 and tags[0].contents[0].name == 'br':
            escape_list[0] = True
        if len(tags[1].contents) == 1 and tags[1].contents[0].name == 'br':
            escape_list[1] = True

        for tag in tags:
            index = tags.index(tag)

            if index == 0 or index == 1:
                if index == 0 and escape_list[0] == True:
                    continue
                if index == 1 and escape_list[1] == True:
                    continue

            ExtraJSON.purify_a(tag)
            ExtraJSON.weichat_purify_img(tag)

            raw += str(tag)
            # string = tag.get_text()

            # if string is not "":
            #     content += tag.get_text() + "\r\n"

            if len(tag.contents) > 1:
                for con in tag:
                    if isinstance(con, Tag):
                        not_format += con.get_text()
            else:
                not_format += tag.get_text()

        raw = raw.encode("UTF-8")

        return (title,raw,not_format,picture)

    def wechat_extra_content_d(self,url):

        # raw = RequestHelper.get(url)
        raw = self.req.get(url)

        soup = BeautifulSoup(raw, "html.parser")
        title = soup.title.text

        pictures = soup.find_all("img", {"data-type": {"jpeg", "png", "gif"}})
        picture = None
        if len(pictures) > 2:
            picture = soup.find("img", {"data-type": {"jpeg", "png", "gif"}}).attrs['data-src']

        # author = soup.find("div", {"class": "rich_media_meta_list"}).children

        tags = soup.find("div", {"class": "rich_media_content", "id": "js_content"}).findAll({"p"})

        if len(tags) < 3:
            tags = soup.find("div", {"class": "rich_media_content", "id": "js_content"}).findAll({"section"})

        # content = ""
        raw = ''
        not_format = ''

        """如果第一或第二个标签是 <p><br/></p> 形式的 删除第一或个标签"""
        escape_list = [False, False]

        if len(tags[0].contents) == 1 and tags[0].contents[0].name == 'br':
            escape_list[0] = True
        if len(tags[1].contents) == 1 and tags[1].contents[0].name == 'br':
            escape_list[1] = True

        for tag in tags:
            index = tags.index(tag)

            if index == 0 or index == 1:
                if index == 0 and escape_list[0] == True:
                    continue
                if index == 1 and escape_list[1] == True:
                    continue

            ExtraJSON.purify_a(tag)
            ExtraJSON.weichat_purify_img(tag)

            raw += str(tag)
            # string = tag.get_text()

            # if string is not "":
            #     content += tag.get_text() + "\r\n"

            if len(tag.contents) > 1:
                for con in tag:
                    if isinstance(con, Tag):
                        not_format += con.get_text()
            else:
                not_format += tag.get_text()

        raw = raw.encode("UTF-8")

        return (title,raw,not_format,picture)

    @staticmethod
    def weichat_purify_img(tag):
        if tag.name == 'img':
            try:
                # print(tag)

                datasrc = tag.attrs['data-src']

                tag.attrs['src'] = datasrc

                # print(" ")
                # print(tag)
            except:
                pass

        for _tag in tag.contents:
            if isinstance(_tag, Tag):
                ExtraJSON.weichat_purify_img(_tag)

    @staticmethod
    def purify_a(tag):
        if tag.name == 'a':
            try:
                # print(tag)

                data_ue_src = tag.attrs['data_ue_src']
                sn = StringHelper.extra_a_to_b(data_ue_src, 'sn=', '&')
                sn = sn[3:len(sn) - 1]

                tag.attrs['data_ue_src'] = sn
                tag.attrs['href'] = sn

                # print(" ")
                # print(tag)
            except:
                pass

        for _tag in tag.contents:
            if isinstance(_tag, Tag):
                ExtraJSON.purify_a(_tag)

    """ 遍历 通过 anyList 获取json 中的所有对象 但是，会被包装成 Element"""
    """startStr 从 startStr 开始提取"""
    """keys 要提取的关键字 比如 title content author 等等"""
    @staticmethod
    def extraAnyList(rawData, startStr, keys):

        index = rawData.index(startStr)

        elementlist = []

        while (1):
            try:
                list = ExtraJSON.anyList(rawData, keys, index)

                if (list[1] == 0):
                    # print("----  Over  ----")

                    break

                elementlist.insert(0, list[2])

                index = list[1]
            except Exception as e:
                LogGo.info(e)
                break

        return elementlist

    """解析 新榜 最新微信 10条 json 结果的 数据"""
    @staticmethod
    def extra_newrank_wechat_list(rawData, keys):
        elementlist = []

        json = demjson.decode(rawData)
        success = json['success']
        value = json['value']

        lastestArticle = value['lastestArticle']

        # trup = ExtraJSON.extra_wechat_list_to_dic_list(keys, list)

        return lastestArticle

    """解析 第一次请求 获取 微信历史 json 结果的 所有微信 列表的 数据"""
    @staticmethod
    def extraWechatList(rawData, startStr, keys):
        start = rawData.index(startStr)
        start = rawData.index("{", start)

        end = rawData.index("}}]}';")
        end = rawData.index("';", end)

        content = rawData[start:end]

        # print(content)

        import html as h
        content = h.unescape(content)# html_parser.unescape()# .unescape(content)
        content = content.replace('\\','')

        # print(txt)

        json = demjson.decode(content)
        list = json['list']

        tuple = ExtraJSON.extra_wechat_list_to_dic_list(keys,list)

        return tuple

    @staticmethod
    def extra_wechat_list_to_dic_list(keys,list):
        elementlist = []
        last_id = ""

        for item in list:
            target = item['app_msg_ext_info']
            comm_target = item['comm_msg_info']
            dic = dict()
            for key in target:
                if keys.count(key) > 0:
                    dic[key] = target[key]

            dic['datetime'] = DateGo.greenToStandard(comm_target['datetime'])
            dic['id'] = comm_target['id']
            last_id = comm_target['id']
            elementlist.append(dic)

            multi = target['multi_app_msg_item_list']
            if len(multi) > 0:
                for mul_msg in multi:
                    mul_dic = dict()
                    for key in mul_msg:
                        if keys.count(key) > 0:
                            mul_dic[key] = mul_msg[key]

                    mul_dic['datetime'] = DateGo.greenToStandard(comm_target['datetime'])
                    elementlist.append(mul_dic)

        return (elementlist, last_id)

    """解析 获取 所提供的 getmassmsglist 返回的 json 结果的 所有微信 列表的 数据"""
    @staticmethod
    def extraGetMassList(rawData, keys):

        elementlist = []

        content = rawData

        json = demjson.decode(content)

        is_continue = json['is_continue']
        list = json['general_msg_list']
        json = demjson.decode(list)
        list = json['list']

        trup = ExtraJSON.extra_wechat_list_to_dic_list(keys, list)

        return (trup[0], trup[1], is_continue)

    @staticmethod
    def extra_any_json(rawData:str, ruler:str, cap=None, list_path:list=None) -> list:
        elementlist = []

        rulers = ExtraHtml.ruler_killer(ruler)
        json = None

        if cap != None:
            if isinstance(cap, list):
                rawData = StringHelper.extra_a_to_b_x(rawData, cap[0], cap[1])
                json = demjson.decode(rawData)
            elif isinstance(cap, str):
                json = demjson.decode(rawData)
                json = ExtraJSON.dic_dip_extra(json, cap)
        else:
            json = demjson.decode(rawData)

            if list_path is not None:
                json = StringHelper.dic_looper(json, list_path)

        for item in json: #循环 json 字典
            try:
                dic = dict()
                for rul in rulers: #循环 ruler 列表
                    res = ExtraJSON.ruler_finder(item, rul[1])
                    if res is not None:
                        dic[rul[0]] = res
                elementlist.append(dic)
            except Exception as e:
                print(e)

        return elementlist

    @staticmethod
    def extra_any_json_dic(rawData, ruler, cap=None):
        elementlist = {}

        rulers = ExtraHtml.ruler_killer(ruler)
        json = None

        if cap != None:
            if isinstance(cap, list):
                rawData = StringHelper.extra_a_to_b_x(rawData, cap[0], cap[1])
                json = demjson.decode(rawData)
            elif isinstance(cap, str):
                json = demjson.decode(rawData)
                json = ExtraJSON.dic_dip_extra(json, cap)
        else:
            json = demjson.decode(rawData)

        # for item in json:
        try:
            for rul in rulers:
                res = ExtraJSON.ruler_finder(json,rul[1])
                if res is not None:
                    elementlist[rul[0]] = res
        except Exception as e:
            print(e)

        return elementlist

    @staticmethod
    def dic_dip_extra(dic, routes):
        """
        按照路线寻找目标
        :param dic: dic
        :param routes: a->b->c
        :return: target
        """

        lis = routes.split('->')

        for node in lis:
            dic = dic[node]

        return dic

    @staticmethod
    def extra_any_json_ex(rawData, ruler, cap=None):
        dic = dict()

        if cap != None:
            rawData = StringHelper.extra_a_to_b_x(rawData, cap[0], cap[1])

        rulers = ExtraHtml.ruler_killer(ruler)
        json = demjson.decode(rawData)

        for key in json:
            try:
                # dic = dict()
                for rul in rulers:
                    res = None
                    if isinstance(json[key], dict):
                        res = ExtraJSON.ruler_finder(json[key], rul[1])
                    elif key == rul[1]:
                        res = json[key]
                    if res is not None:
                        dic[rul[0]] = res
                # elementlist.append(dic)
            except Exception as e:
                print(e)

        return dic

    @staticmethod
    def dic_to_list(dic, list, par=None):
        """打散字典，按照元素出现的次序排序成列表方便遍历"""

        if par is None:
            par = ''

        for key in dic:
            if isinstance(dic[key], dict):
                ExtraJSON.dic_to_list(dic[key], list, par = par + ' ' + key)
            else:
                list.insert(0, par + ' ' + key + ' ' + str(dic[key]))

    "status:status;token:token"
    @staticmethod
    def go_json(rawData, ruler, cap=None):
        """单条json 提取"""
        dic = dict()

        if cap != None:
            rawData = StringHelper.extra_a_to_b_x(rawData, cap[0], cap[1])

        rulers = ExtraHtml.ruler_killer_ex(ruler)
        json = demjson.decode(rawData)

        list = []
        ExtraJSON.dic_to_list(json, list)

        for item in list:
            for ruler in rulers:
                if item.count(ruler[1]) > 0:
                    dic[ruler[0]] = StringHelper.cut_head(item, ruler[1] + ' ')
                    continue

        return dic

    @staticmethod
    def ruler_finder(dic, key):
        """貌似是 json 的提取函数"""
        result = None

        if key == '' or dic is None:
            return None

        # 遍历取出所有匹配内容
        if key.count('*loop ') == 1:
            # key = StringHelper.cutfrom(key, '*loop ')
            looplist = key.split(' ', 1)[1]

            if looplist.count('->') > 0:
                loop_part = looplist.split('->')
                try:
                    dic = dic[loop_part[0]]
                    loop_part.remove(loop_part[0])

                    if len(loop_part) > 1:
                        looplist = '->'.join(loop_part)
                        key = ' '.join(('*loop', looplist))
                    else:
                        key = '*loop ' + loop_part[0]

                    return ExtraJSON.ruler_finder(dic, key)
                except Exception as e:
                    print(e)
            else:
                list = []
                for sub in dic:
                    try:
                        value = sub[looplist]
                        list.append(value)
                    except Exception as e:
                        print(e)
                if len(list) > 0:
                    result = list
        # 没有 *loop 就代表不需要遍历，那么取出第一个匹配项就可
        elif key.count('->') > 0:
            loop_part = key.split('->')
            try:
                dic = dic[loop_part[0]]
                loop_part.remove(loop_part[0])

                if len(loop_part) > 1:
                    _key = '->'.join(loop_part)
                    return ExtraJSON.ruler_finder(dic, _key)
                else:
                    # 判断最后的节点是否为列表
                    if isinstance(dic, dict):
                        return dic[loop_part[0]]
                    else:
                        return dic[0][loop_part[0]]
            except Exception as e:
                print(e)
        # 只需查找根节点
        elif key.count(' ') == 0:
            try:
                result = dic[key]
            except:
                pass

        return result

    def ruler_finder_arrow_loop(self, dic):
        pass


    """
    微博
    解析 获取 所提供的 getmassmsglist 返回的 json 结果的 所有微信 列表的 数据
    """
    @staticmethod
    def extra_getindex_list(rawData, keys):

        elementlist = []

        content = rawData

        json = demjson.decode(content)

        data = json['data']

        # cardlistinfo = json['cardlistinfo']

        cards = data['cards']

        # ok = json['ok']
        # scheme = json['scheme']

        # seeLevel = json['seeLevel']

        if len(cards) == 0:
            return elementlist

        for card in cards:
            card_type = card['card_type']

            if card_type != 9:
                continue

            mblog = card['mblog']

            try:
                retweeted_status = mblog['retweeted_status']
                mblog['retweeted_status'] = retweeted_status
            except Exception as e:
                pass

            elementlist.append(mblog)

        #过滤各种标签
        for card in elementlist:
            text = card['text']

            # try:
            #     LogGo.info(card['id'])
            #     print("weibo id: " + card['id'])
            # except Exception as e:
            #     pass

            # print(text)
            # print("       ")

            # 过滤 <a class='k' 标签(颜符号)
            while True:
                try:
                    staStr = "<a class='k'"
                    staIndex = text.index(staStr)
                    endStr = "</a>"
                    endIndex = text.index(endStr, staIndex) + len(endStr)

                    tag_a = text[staIndex:endIndex]

                    sharpStr = '#'
                    tarStrInd = tag_a.index(sharpStr)
                    tarEndInd = tag_a.index(sharpStr,tarStrInd + 1) + len(sharpStr)

                    target = tag_a[tarStrInd:tarEndInd]

                    start = text[0:staIndex]
                    end = text[endIndex:len(text)]

                    text = start + target + end

                except Exception as e:
                    break

            # 过滤 i标签(颜符号)
            while True:
                try:
                    staStr = "<i class"
                    staIndex = text.index(staStr)
                    endStr = "</i>"
                    endIndex = text.index(endStr,staIndex) + len(endStr)
                    sta = text[0:staIndex]
                    end = text[endIndex:len(text)]

                    text = sta + end
                except Exception as e:
                    break

            # 过滤 <br/>
            while True:
                try:
                    staStr = "<br/>"
                    staIndex = text.index(staStr)
                    sta = text[0:staIndex]
                    end = text[staIndex + len(staStr):len(text)]

                    text = sta + end
                except Exception as e:
                    break

            # 过滤 <a data-url 标签
            while True:
                try:
                    staStr = "<a data-url"
                    staIndex = text.index(staStr)
                    endStr = "</a>"
                    endIndex = text.index(endStr, staIndex) + len(endStr)

                    sta = text[0:staIndex]
                    end = text[endIndex:len(text)]

                    text = sta + end

                except Exception as e:
                    break

            # 过滤 @标签
            while True:
                try:
                    staStr = "<a href"
                    staIndex = text.index(staStr)
                    endStr = "</a>"
                    endIndex = text.index(endStr, staIndex) + len(endStr)

                    tag_a = text[staIndex:endIndex]

                    atStr = '@'
                    tarStrInd = tag_a.index(atStr)
                    tarEndInd = tag_a.index(endStr, tarStrInd)

                    target = tag_a[tarStrInd:tarEndInd]

                    start = text[0:staIndex]
                    end = text[endIndex:len(text)]

                    text = start + target + end

                except Exception as e:
                    break

            # 过滤 普通超链接　这个需要放在 过滤 ＠标签后
            while True:
                try:
                    staStr = "<a href"
                    staIndex = text.index(staStr)
                    endStr = "</a>"
                    endIndex = text.index(endStr, staIndex) + len(endStr)

                    start = text[0:staIndex]
                    end = text[endIndex:len(text)]

                    text = start + end

                except Exception as e:
                    break

            # 过滤 <span 标签
            while True:
                try:
                    staStr = "<span class"
                    staIndex = text.index(staStr)
                    endStr = "</span>"
                    endIndex = text.index(endStr, staIndex) + len(endStr)

                    start = text[0:staIndex]
                    end = text[endIndex:len(text)]

                    text = start + end

                except Exception as e:
                    break

            try:
                staStr = "<"
                staIndex = text.index(staStr)

                # LogGo.warning("微博正文内容过滤不完整：" + text)

            except Exception as e:
                pass

            card['text'] = text
            # print(card['text'])
            # print("                  ")

        #过滤 created_at
        for card in elementlist:
            created_at = None
            try:
                created_at = card['created_at']
            except Exception as e:
                pass

            if created_at is None:return

            created_at = str(created_at)

            if created_at.count("分钟前") > 0:
                index = created_at.index("分钟前")
                created_at = created_at[0:index]

                created_at = int(created_at)
                created_at = DateGo.date_befor_minutes(created_at)

                card['created_at'] = created_at

                continue

            elif created_at.count("小时前") > 0:
                index = created_at.index("小时前")
                created_at = created_at[0:index]

                created_at = int(created_at)
                created_at = DateGo.date_befor_hours(created_at)

                card['created_at'] = created_at

                continue

            elif created_at.count('今天') > 0:
                try:
                    time = created_at.split(' ',1)[1]
                    time_pair = time.split(':',1)

                    # now = datetime.datetime.now()
                    # dest = datetime.datetime(now.year, now.month, now.day, int(time_pair[0]), int(time_pair[1]))

                    dest = DateGo.time_to_date(hours=int(time_pair[0]),minutes=int(time_pair[1]))

                    card['created_at'] = dest

                    continue
                except Exception as e:
                    print(e)
                    continue

            elif created_at.count('昨天') > 0:
                try:
                    time = created_at.split(' ',1)[1]
                    time_pair = time.split(':',1)

                    dest = DateGo.time_to_date(day=-1,hours=int(time_pair[0]),minutes=int(time_pair[1]))

                    card['created_at'] = dest

                    continue
                except Exception as e:
                    print(e)
                    continue

            elif created_at.count('刚刚') > 0:
                try:
                    dest = DateGo.time_to_date()

                    card['created_at'] = dest

                    continue
                except Exception as e:
                    print(e)
                    continue

            elif created_at.count('-') == 1:
                try:
                    pair = created_at.split('-')

                    month = pair[0]
                    day = pair[1]

                    dest = DateGo.time_to_date(month=month, day=day)

                    card['created_at'] = dest

                    continue
                except Exception as e:
                    print(e)
                    continue

            try:
                time_pair = created_at.split(' ', 1)
                months = time_pair[0].split('-')
                times = time_pair[1].split(':')

                month = months[0]
                day = months[1]

                hours = times[0]
                minutes = times[1]

                dest = DateGo.time_to_date(int(month), int(day), int(hours), int(minutes))

                card['created_at'] = dest
            except Exception as e:
                continue

        """处理 pics"""
        for card in elementlist:
            _pics = []

            try:
                pics = card['pics']
                for pic in pics:
                    large = pic['large']
                    url = large['url']
                    _pics.append(url)

            except Exception as e:
                pass

            card['pics'] = _pics

        return (elementlist)



    """采集json中的 一个元素 返回一个 Element"""""
    """采集json中的 列表形式的数据。 keys 为键序列 start 为 json 字符串 中要开始采集的游标位置"""""
    """返回类型为元祖"""""
    @staticmethod
    def anyList(rawData, keys, start):
        par_list = keys

        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        con = []
        offect = start

        dic = dict()

        for key in par_list:
            try:
                content = ExtraJSON.getContent(rawData, key, offect)
                con.append(content)

                offect += content[1]
                # print(key + " : " + content[0])

                dic[key] = content[0]
            except Exception as e:
                LogGo.warning(e)
                continue

        # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        # print("                                                 ")

        minLen = 0

        for i in con:
            minLen += i[1]

        try:
            nextIndex = rawData.index(keys[0], start + minLen)
        except ValueError as e:
            #LogGo.warning(e)
            return (con, 0)

        return (con, nextIndex, dic)

    """在 json 数据中，根据提供的 key 返回 value {key:value}"""""
    @staticmethod
    def getContent(rawData, key, start):

        authorIndex = rawData.index(key, start)
        contentEndIndex = rawData.index("\"", authorIndex + len(key) + 3)

        content = rawData[authorIndex + len(key) + 3:contentEndIndex]

        test = rawData[authorIndex :contentEndIndex]

        return (content, contentEndIndex - authorIndex)

    """循环 找到最后的 括号"}" 用来做 json 解析"""
    @staticmethod
    def getContentEx(rawData, key, start):

        start = rawData.index("msgList")
        start = rawData.index("{", start)

        end = rawData.index("]};")
        end = rawData.index(";", end)

        content = rawData[start:end]

        json = demjson.decode(content)
        list = json['list']

        print(content)


# json = ''
# try:
#     import json
#     target = json.loads(raw)
#
#     json = demjson.decode(raw)
# except Exception as e:
#      print(str(e))
# print(json)