import demjson
import time
import datetime
import os

from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import NavigableString
from bs4.element import Comment

from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_class_ver import RequestHelperClassVer
from CoTec.utility.date.date_go import DateGo
from CoTec.utility.string.string_go import StringHelper
from CoTec.core.exception.exception_go import *
from CoTec.utility.string.string_go import StringHelper as Sh


class RulerExtra(object):
    @staticmethod
    def canwecom(a, b):
        """
        合并
        :param a:
        :param b:
        :return:
        """
        res = ''

        if a.startswith('http'):
            if b.startswith('http'):
                res = b
            else:
                res = a + b
        else:
            res = a + b

        return res


class ExtraHtml(object):
    """根据数据库动态调整"""

    # """返回结果为 元组"""
    # @staticmethod
    # def wechat_extra_content(url):
    #
    #     raw = RequestHelper.get(url)
    #
    #     soup = BeautifulSoup(raw, "html.parser")
    #     title = soup.title.text
    #
    #     picture = soup.find("img", {"data-type": {"jpeg", "png", "gif"}}).attrs['data-src']
    #
    #     author = soup.find("div", {"class": "rich_media_meta_list"}).children
    #
    #     tags = soup.find("div", {"class": "rich_media_content", "id": "js_content"}).findAll("p")
    #
    #     content = ""
    #     raw = ""
    #
    #     """如果第一个标签是 <p><br/></p> 形式的 删除第一个标签"""
    #     escape = False
    #     if len(tags[0].contents) == 1 and tags[0].contents[0].name == 'br':
    #         escape = True
    #
    #     for tag in tags:
    #         if escape:
    #             escape = False
    #             continue
    #
    #         string = tag.get_text()
    #         raw += str(tag)
    #
    #         if string is not "":
    #             content += tag.get_text() + "\r\n"
    #
    #     # print("title: Due to linux encode problem ,the content can`t be displayed.")
    #     # print("title: " + title)
    #
    #     # raw = tags.string
    #     # print(raw)
    #     raw = raw.encode("UTF-8")
    #
    #     #content = content.encode("UTF-8")
    #
    #     #print(content)
    #
    #     return (title,raw,content,picture)

    # @staticmethod
    # def test():
    #

    req = RequestHelperClassVer()


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



    """在 json 数据中，根据提供的 key 返回 value {key:value}"""""
    @staticmethod
    def getContent(rawData, key, start):

        authorIndex = rawData.index(key, start)
        contentEndIndex = rawData.index("\"", authorIndex + len(key) + 3)

        content = rawData[authorIndex + len(key) + 3:contentEndIndex]

        # test = rawData[authorIndex :contentEndIndex]

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

    """
    容器必须是 ul 的直接或间接 上级容器
    """
    @staticmethod
    def ul_finder(raw, dics):
        soup = BeautifulSoup(raw, "html.parser")
        # lis = soup.find("div", {"class": class_name}).find_all('ul')
        lis = soup.find("div", dics).find_all('ul')

        tar = []

        for tag in lis:
            li = tag.find_all('li')

            for item in li:
                nav = []
                for content in item.contents:
                    if isinstance(content,Tag):
                        nav.append(content)

                tar.append(nav)

        return tar

    @staticmethod
    def any_list_finder(raw, container_div_attr, target_attr_tuple):
        from bs4.element import Tag

        soup = BeautifulSoup(raw, "html.parser")
        lis = soup.find("div", container_div_attr).find_all(target_attr_tuple[0],target_attr_tuple[1])

        tar = []

        for tag in lis:
            nav = []
            for content in tag.contents:
                if isinstance(content, Tag):
                    nav.append(content)

            tar.append(nav)

        return tar

    @staticmethod
    def any_list_finder_ex(raw, container_div_attr, target_attr_tuple):
        """
        提取页面元素成为 tag list
        :param raw:
        :param container_div_attr: 容器特征 (div,[class:channelLeftPart])
        :param target_attr_tuple: 列表特征 (li,[])
        :return: tag list
        """
        from bs4.element import Tag

        soup = BeautifulSoup(raw, "html.parser")
        lis = soup.find(container_div_attr[0], container_div_attr[1]).find_all(target_attr_tuple[0],target_attr_tuple[1])

        tar = []

        for tag in lis:
            nav = []
            for content in tag.contents:
                if isinstance(content, Tag):
                    ExtraHtml.loop_tag(nav, content)

            tar.append(nav)

        return tar

    @staticmethod
    def list_page(raw):
        from bs4.element import Tag

        soup = BeautifulSoup(raw, "html.parser")
        contents = soup.contents

        tar = []

        for tag in contents:
            if isinstance(tag, Tag):
                for content in tag.contents:
                    if isinstance(content, Tag):
                        ExtraHtml.loop_tag(tar, content)

        return tar

    """
    通过递归遍历把 数据结构 从树状变为 线性
    """
    @staticmethod
    def loop_tag(list, tag):
        list.append(tag)

        contents = tag.contents
        count = len(contents)

        if count > 0:
            for _tag in contents:
                if isinstance(_tag, Tag):
                    ExtraHtml.loop_tag(list, _tag)

    @staticmethod
    def tag_list_to_ruler_list_ex(list, ruler, need_tag=False):
        # result = []
        dic = dict()
        if len(list) < 1:
            return dic

        ruler_list = ExtraHtml.ruler_killer(ruler)
        check_list = []
        for ruler_pair in ruler_list:
            for tag in list:
                skip = False
                res = ExtraHtml.ruler_finder_ex(tag, ruler_pair, need_tag)
                if res is not None:
                    for cus in check_list:
                        if cus[0] == ruler_pair[1] and cus[1] == res[1]:
                            skip = True
                            break

                    if skip:
                        continue

                    if need_tag:
                        return res[1]

                    dic[res[0]] = res[1]
                    check_list.append((ruler_pair[1], res[1]))
                    break
        return dic

    @staticmethod
    def ruler_finder_condition_next_sibling(ruler0: str) -> bool:
        """
        判断 是否要提取 tag 的 nextSilbing
        :param ruler:
        :return:
        """
        type = '-'

        result = False

        try:
            if ruler0.count(type) == 1:
                result = True
        except:
            pass

        return result

    @staticmethod
    def ruler_finder_condition_content(ruler:str, extract=False) -> bool:
        """
        判断 ruler 是否为 [你好]
        :param ruler:
        :return:
        """
        type1 = '['
        type2 = ']'

        result = False

        try:
            if ruler.count(type1) == 1 and ruler.count(type2) == 1 and ruler.startswith(type1):
                if extract:
                    result = Sh.extra_a_to_b_x(ruler, type1, type2)
                else:
                    result = True
        except:
            pass

        if result is False and extract:
            raise Exception("未找到指定 字符")

        return result

    @staticmethod
    def ruler_finder_condition(ruler):
        """
        依据 ruler2 判断 ruler 是什么类型 直接查找 依据父属性查找 循环遍历 等
        :param ruler:
        :return:
        """
        type = 'no'

        try:
            if ruler.count('@') == 1:
                type = 'at_loop'
        except:
            pass

        return type

    @staticmethod
    def ruler_finder_multi_at(tag, ruler2):
        result = None
        pair = ruler2.split('@', 1)

        tup = Sh.str_to_dictup(pair[1])
        _tag = tup[0]
        dic = tup[1]
        parent_container = (_tag, dic)

        tup = Sh.str_to_dictup(pair[0])
        _tag = tup[0]
        dic = tup[1]
        list_tup = (_tag, dic)

        p_tag = parent_container[0]
        p_dic = parent_container[1]
        s_ruler = ''

        for key in p_dic:
            s_ruler = p_tag + ' ' + key + '=' + p_dic[key]
            break
        ruler_pair = ('', s_ruler)

        ruler_pair_part_of = ruler_pair[1].split(' ', 2)
        identify = ruler_pair_part_of[1].split('=', 1)
        if tag.name != ruler_pair_part_of[0]:
            return result

        try:
            if tag.attrs[identify[0]] == identify[1]:
                result = []
                raw = str(tag)

                # 获取 list 提取成 字典
                list = ExtraHtml.any_list_finder_ex(raw, parent_container, list_tup)

                for item in list:
                    if len(item) < 1:
                        continue

                    dic_list = ExtraHtml.tag_list_to_ruler_list_ex(item, ruler)

                    result.append(dic_list)

                return result
        except:
            result = None

        return result

    @staticmethod
    def ruler_finder_recursion_dig_for_p(tag, val):
        dead_list = ['script', 'style', 'span', 'i', 'iframe']

        if not isinstance(tag, Tag):
            return

        for child in tag.contents:
            if isinstance(child, Comment):
                continue
            elif isinstance(child, NavigableString):
                val.append(str(child))
            elif isinstance(child, Tag):
                if child.name in dead_list:
                    continue
                else:
                    ExtraHtml.ruler_finder_recursion_dig_for_p(child, val)

    @staticmethod
    def finder_ruler_memory(ruler:str):
        """
        暂存 ruler 避免被循环修改
        :param ruler:
        :return:
        """
        if ExtraHtml.ruler is None:
            ExtraHtml.ruler = ruler

    @staticmethod
    def ruler_finder_ex(tag, ruler_pair, need_tag=False):
        """
        html 页面元素抓取核心函数
        :param tag: 待遍历 的 soup tag 元素
        :param ruler_pair: 元素寻找规则
        :param need_tag: 如果为 true 则返回 找到的 子 tag 元素
        :return:
        """

        result = None
        ruler2 = ruler_pair[1]

        next_sibling = False

        # 判断是否需要获取 nextSibling
        if ExtraHtml.ruler_finder_condition_next_sibling(ruler_pair[0]):
            next_sibling = True

        # 通过标签中间的内容判断 <span>你好</span> 则 ruler 为 [你好]
        if ExtraHtml.ruler_finder_condition_content(ruler2):
            try:
                if tag.get_text() == ExtraHtml.ruler_finder_condition_content(ruler2, True):
                    if next_sibling:
                        result = ExtraHtml.finder_need_tag(tag, need_tag, next_sibling=True, ruler_pair=ruler_pair)
                    else:
                        result = (ruler_pair[0], ExtraHtml.finder_need_tag(tag, need_tag))

                    return result
            except:
                pass
        #在某个父tag 下取得所有相同类型的子tag
        # 这个好像是个废掉的功能
        elif ExtraHtml.ruler_finder_condition(ruler2) == 'at_loop':
            re = ExtraHtml.ruler_finder_multi_at(tag, ruler2)

            if re is not None:
                result = (ruler_pair[0], re)
                return result
        #依据父属性做查找
        elif ruler_pair[1].count(':') > 0 and ruler_pair[1].count(':') > ruler_pair[1].count('http:'):
            status = False
            _pair = ruler_pair[1].split(':', 1)
            name = _pair[0]#可能 是子标签
            name_part = []

            if name.count(' ') > 0:#可能 有属性
                name_part = name.split(' ', 1)#可能 属性
                name = name_part[0]#可能 标签

            if tag.name != name:#可能 不是此标签，跳过
                return None

            # 可能 父标签部分
            parent_pair = _pair[1].split(' ', 1)
            # 可能 父标签名
            parent_name = parent_pair[0]

            # 可能 被遍历的tag没有父元素 或者 父元素 不是 tag 或者 父元素名不对 跳过
            if tag.parent == None or not isinstance(tag.parent, Tag) or tag.parent.name != parent_name:
                return None

            # 可能 没有添加属性 那么 父元素的要求已达到
            if len(parent_pair) == 1:
                status = True

            # 父标签的属性
            parent_attr = parent_pair[1].split('=', 1)

            # 可能* 如果有父标签的属性 或者 等号后为空
            if len(parent_attr) == 1 or (len(parent_attr) > 1 and parent_attr[1] == None or parent_attr[1] == ''):
                try:
                    attr = tag.parent.attrs[parent_attr[0]]
                    status = True
                except:
                    pass

            if len(parent_attr) > 1 and parent_attr[1] != None or parent_attr[1] != '' :
                try:
                    if ' '.join(tag.parent.attrs[parent_attr[0]]) == parent_attr[1]:
                        status = True
                except:
                    pass

            if status:
                if len(name_part) > 1 and name_part[1] != None and name_part != '':
                    return ExtraHtml.ruler_finder_ex(tag,(ruler_pair[0], _pair[0]), need_tag)
                else:
                    # result = (ruler_pair[0], tag.text)
                    result = (ruler_pair[0], ExtraHtml.finder_need_tag(tag, need_tag))

        #依据自身属性
        elif ruler_pair[1].count(' ') > 0 or ruler_pair[1].count('=') == 2:
            if ruler_pair[1].count('=') == 2:
                ruler_pair_part_of = ruler_pair[1].split(' ', 2)
                identify = ruler_pair_part_of[2].split('=', 1)

                if tag.name != ruler_pair_part_of[0]:
                    return None

                try:
                    if tag.attrs[identify[0]] == identify[1]:
                        return ExtraHtml.ruler_finder_ex(tag, (ruler_pair[0], ruler_pair_part_of[0] + ' ' + ruler_pair_part_of[1]), need_tag)
                except:
                    pass
            else:
                _pair = ruler_pair[1].split(' ', 1)
                _name = _pair[0]

                next_flag = False

                if _name.count('^') == 1:
                    next_flag = True
                    _name = Sh.cut_head(_name, '^')

                if tag.name != _name:
                    return None

                # 关键字查询
                keyword = Sh.extra_a_to_b_x(_pair[1], '[', ']')
                if _pair[1].count('[') == 1 and _pair[1].count(']') == 1:
                    if keyword in tag.text and len(tag.contents) <= 1:
                        if next_flag:
                            # return (ruler_pair[0], tag.next_sibling.text)
                            return (ruler_pair[0], ExtraHtml.finder_need_tag(tag, need_tag, True))
                        else:
                            # return (ruler_pair[0], tag.text)
                            return (ruler_pair[0], ExtraHtml.finder_need_tag(tag, need_tag))

                equ_pair = _pair[1].split('=',1)

                _attr = equ_pair[0]

                val = StringHelper.extra_a_to_b(_attr, '(', ')')
                _attr = StringHelper.delete_piece(_attr, val)

                for item in equ_pair:
                    if item == '':
                        equ_pair.remove(item)

                if len(equ_pair) > 1:
                    value = equ_pair[1]

                    try:
                        att = tag.attrs[_attr]
                        _value = ''
                        if isinstance(att, str):
                            _value = att
                        elif isinstance(att, list):
                            _value = " ".join(tag.attrs[_attr])
                        if _value == value:
                            # result = (ruler_pair[0], tag.text)
                            result = (ruler_pair[0], ExtraHtml.finder_need_tag(tag, need_tag))
                    except:
                        pass
                else:
                    try:
                        val = val[1:len(val) - 1]

                        ed = tag.attrs[_attr]
                        op = val
                        # com = op + ed
                        com = RulerExtra.canwecom(op, ed)

                        result = (ruler_pair[0], com)
                    except:
                        return None
                # return (ruler_pair[0], tag.attrs[_attr])

        # 不通过属性 直接查找
        else:
            if tag.name == ruler_pair[1]:
                if tag.text is not None and tag.text != '':
                    # result = (ruler_pair[0], tag.text)
                    result = (ruler_pair[0], ExtraHtml.finder_need_tag(tag, need_tag))

        # 星判断
        if result != None and len(result) > 1 and result[0].count('*') > 0:
            key = ''
            value = ''
            value_list = []
            if ruler_pair[0].count('*') > 0:
                if len(tag.contents) > 1:#多重判断
                    for con in tag:
                        if isinstance(con, Tag):
                            #提取p标签
                            if ruler_pair[0].count('***') == 1:
                                if con.name == 'p':
                                    # value += con.get_text()
                                    # value += ExtraHtml.ruler_finder_recursion_dig_for_p(con)
                                    ExtraHtml.ruler_finder_recursion_dig_for_p(con, value_list)
                            # 删除所有标签
                            elif ruler_pair[0].count('**') == 1:
                                value += con.get_text()
                            # 保留标签
                            elif ruler_pair[0].count('*') == 1:
                                value += str(con)

                else:#单tag 判断
                    if ruler_pair[0].count('**') == 1:
                        value += tag.get_text()
                    elif ruler_pair[0].count('*') == 1:
                        value += str(tag)

                #善后
                if ruler_pair[0].count('***') == 1:
                    # value = "".join(value.split())
                    value = "".join(value_list)
                    value = "".join(value.split())
                    key = StringHelper.cutfrom(ruler_pair[0], '***')
                elif ruler_pair[0].count('**') == 1:
                    value = "".join(value.split())
                    key = StringHelper.cutfrom(ruler_pair[0], '**')
                elif ruler_pair[0].count('*') == 1:
                    key = StringHelper.cutfrom(ruler_pair[0], '*')

            elif ruler_pair[0].count('^') > 0:
                value = tag.text
                value = "".join(value.split())
                key = StringHelper.cutfrom(ruler_pair[0], '^')
            else:
                key = ruler_pair[0]
                value = tag.text

            if value == '':
                print('info: in ruler_finder_ex star filter -> ' + result[0] + ' got empty result!')
                value = result[1]

            return (key, value)
        elif result == None:
            return None
        else:
            return result

    @staticmethod
    def finder_need_tag(tag, need_tag=False, next_sibling=False, next_sibling_text=False, get_text=False, ruler_pair:()=None):
        if need_tag:
            return tag
        elif next_sibling_text:
            return tag.next_sibling.text
        elif next_sibling:
            if ruler_pair is not None:
                ruler_pair[0] = Sh.cut_tail(ruler_pair[0], '-')
                return (ruler_pair[0], str(tag.next_sibling))
        elif get_text:
            return tag.get_text()
        else:
            return tag.text

    @staticmethod
    def ruler_is_nextline(ruler1, tag):
        return False

    @staticmethod
    def ruler_killer(ruler):
        ruler_lis = []
        ruler_pair = ruler.split(';')

        for pair in ruler_pair:
            tmp = pair.split(':',1)
            ruler_lis.append(tmp)

        return ruler_lis

    @staticmethod
    def ruler_killer_ex(ruler):
        ruler_lis = []
        ruler_pair = ruler.split(';')

        for pair in ruler_pair:
            tmp = pair.split(':',1)
            ruler_lis.append((tmp[0], tmp[1], 0))

        return ruler_lis

    def get_page_encode(self, url):
        try:
            raw = self.req.get(url)

            encode = StringHelper.extra_equ_value(raw, 'charset', '"')
            encode = StringHelper.cutfrom(encode,'/')

            return encode
        except HttpConnectionFailedException as e:
            raise e
        except:
            return ''

    @staticmethod
    def get_txt_page_encode(raw:str) -> str:
        try:
            encode = StringHelper.extra_equ_value(raw, 'charset', '"')
            encode = StringHelper.cutfrom(encode, '/')

            return encode
        except HttpConnectionFailedException as e:
            raise e
        except:
            return ''

    """微信正文内容抓取函数，正式中会尽量根据数据库动态调整"""
    """返回结果为 元组"""
    # @staticmethod
    # def web_extra_content(url, ruler, encode):
    #
    #     ruler_list = ExtraHtml.ruler_killer(ruler)
    #     raw = RequestHelper.get(url, encode=encode)
    #
    #     soup = BeautifulSoup(raw, "html.parser")
    #     title = soup.title.text
    #
    #     list = ExtraHtml.list_page(raw)
    #
    #
    #     new_list = []
    #
    #     for tag in list:
    #         if tag.name == 'div':
    #             try:
    #                 if tag.attrs['class'][0] == 'post_time_source':
    #                     new_list.append(tag)
    #                     break
    #             except:
    #                 pass
    #
    #     dic_list = ExtraHtml.tag_list_to_ruler_list_ex(new_list, ruler)
    #
    #     return dic_list

    def web_extra_content(self, url, ruler, encode):
        """
        提取页面元素
        :param url:
        :param ruler:
        :param encode:
        :return:
        """
        # ruler_list = ExtraHtml.ruler_killer(ruler)
        raw = self.req.get(url, encode=encode)

        # soup = BeautifulSoup(raw, "html.parser")
        # title = soup.title.text

        list = ExtraHtml.list_page(raw)

        dic_list = ExtraHtml.tag_list_to_ruler_list_ex(list, ruler)

        return dic_list

    def web_extra_tag(self, url, tag_ruler, encode):
        raw = self.req.get(url, encode=encode)

        list = ExtraHtml.list_page(raw)

        tag = ExtraHtml.tag_list_to_ruler_list_ex(list, tag_ruler, True)
        return tag

    def extract_pure_text(self, url, encode=None):
        raw = self.req.get(url, encode=encode)

        return raw

    def extract_dic_list_from_page(self, result, url, parent_attr, list_attr, ruler, exists:list=None, encode:str=None):
        """
        从页面提取 dic 列表
        :param result: 结果列表
        :param raw:
        :param exists:
        :param ruler: 字典规则
        :param parent_attr: parent_container attribute
        :param list_attr: list attribute
        """
        raw = self.req.get(url, encode=encode)

        tup = Sh.str_to_dictup(parent_attr)
        tag = tup[0]
        dic = tup[1]
        parent_container = (tag, dic)

        tup = Sh.str_to_dictup(list_attr)
        tag = tup[0]
        dic = tup[1]
        list_tup = (tag, dic)

        # 获取 list 提取成 字典
        list = ExtraHtml.any_list_finder_ex(raw, parent_container, list_tup)

        for item in list:
            if len(item) < 1:
                continue

            dic_list = ExtraHtml.tag_list_to_ruler_list_ex(item, ruler)

            """抓取时的重复验证"""
            if exists is not None:
                if exists.count(dic_list['link']) < 1:
                    result.append(dic_list)
                else:
                    break
            else:
                result.append(dic_list)





# 备份 1204
# @staticmethod
#     def ruler_finder_ex(tag, ruler_pair, need_tag=False):
#         result = None
#         ruler2 = ruler_pair[1]
#
#         #在某个父tag 下取得所有相同类型的子tag
#         # 这个好像是个废掉的功能
#         if ExtraHtml.ruler_finder_condition(ruler2) == 'at_loop':
#             re = ExtraHtml.ruler_finder_multi_at(tag, ruler2)
#
#             if re is not None:
#                 result = (ruler_pair[0], re)
#                 return result
#         #依据父属性做查找
#         elif ruler_pair[1].count(':') > 0 and ruler_pair[1].count(':') > ruler_pair[1].count('http:'):
#             status = False
#             _pair = ruler_pair[1].split(':', 1)
#             name = _pair[0]#可能 是子标签
#             name_part = []
#
#             if name.count(' ') > 0:#可能 有属性
#                 name_part = name.split(' ', 1)#可能 属性
#                 name = name_part[0]#可能 标签
#
#             if tag.name != name:#可能 不是此标签，跳过
#                 return None
#
#             parent_pair = _pair[1].split(' ', 1)#可能 父标签部分
#             parent_name = parent_pair[0]#可能 父标签名
#
#             if tag.parent == None or not isinstance(tag.parent, Tag) or tag.parent.name != parent_name:#可能 被遍历的tag没有父元素 或者 父元素 不是 tag 或者 父元素名不对 跳过
#                 return None
#
#             if len(parent_pair) == 1:#可能 没有添加属性 那么 父元素的要求已达到
#                 status = True
#
#             parent_attr = parent_pair[1].split('=', 1)#父标签的属性
#
#             if len(parent_attr) == 1 or (len(parent_attr) > 1 and parent_attr[1] == None or parent_attr[1] == ''):#可能* 如果有父标签的属性 或者 等号后为空
#                 try:
#                     attr = tag.parent.attrs[parent_attr[0]]
#                     status = True
#                 except:
#                     pass
#
#             if len(parent_attr) > 1 and parent_attr[1] != None or parent_attr[1] != '' :
#                 try:
#                     if ' '.join(tag.parent.attrs[parent_attr[0]]) == parent_attr[1]:
#                         status = True
#                 except:
#                     pass
#
#             if status:
#                 if len(name_part) > 1 and name_part[1] != None and name_part != '':
#                     return ExtraHtml.ruler_finder_ex(tag,(ruler_pair[0], _pair[0]))
#                 else:
#                     result = (ruler_pair[0], tag.text)
#
#         #依据自身属性
#         elif ruler_pair[1].count(' ') > 0 or ruler_pair[1].count('=') == 2:
#             if ruler_pair[1].count('=') == 2:
#                 ruler_pair_part_of = ruler_pair[1].split(' ', 2)
#                 identify = ruler_pair_part_of[2].split('=', 1)
#
#                 if tag.name != ruler_pair_part_of[0]:
#                     return None
#
#                 try:
#                     if tag.attrs[identify[0]] == identify[1]:
#                         return ExtraHtml.ruler_finder_ex(tag, (ruler_pair[0], ruler_pair_part_of[0] + ' ' + ruler_pair_part_of[1]))
#                 except:
#                     pass
#             else:
#                 _pair = ruler_pair[1].split(' ', 1)
#                 _name = _pair[0]
#
#                 next_flag = False
#
#                 if _name.count('^') == 1:
#                     next_flag = True
#                     _name = Sh.cut_head(_name, '^')
#
#                 if tag.name != _name:
#                     return None
#
#                 # 关键字查询
#                 keyword = Sh.extra_a_to_b_x(_pair[1], '[', ']')
#                 if _pair[1].count('[') == 1 and _pair[1].count(']') == 1:
#                     if keyword in tag.text and len(tag.contents) <= 1:
#                         if next_flag:
#                             return (ruler_pair[0], tag.next_sibling.text)
#                         else:
#                             return (ruler_pair[0], tag.text)
#
#                 equ_pair = _pair[1].split('=',1)
#
#                 _attr = equ_pair[0]
#
#                 val = StringHelper.extra_a_to_b(_attr, '(', ')')
#                 _attr = StringHelper.delete_piece(_attr, val)
#
#                 for item in equ_pair:
#                     if item == '':
#                         equ_pair.remove(item)
#
#                 if len(equ_pair) > 1:
#                     value = equ_pair[1]
#
#                     try:
#                         att = tag.attrs[_attr]
#                         _value = ''
#                         if isinstance(att, str):
#                             _value = att
#                         elif isinstance(att, list):
#                             _value = " ".join(tag.attrs[_attr])
#                         if _value == value:
#                             result = (ruler_pair[0], tag.text)
#                             # return (ruler_pair[0], tag.text)
#                     except:
#                         pass
#                 else:
#                     try:
#                         val = val[1:len(val) - 1]
#
#                         ed = tag.attrs[_attr]
#                         op = val
#                         # com = op + ed
#                         com = RulerExtra.canwecom(op, ed)
#
#                         # return (ruler_pair[0], com)
#                         result = (ruler_pair[0], com)
#                     except:
#                         return None
#                 # return (ruler_pair[0], tag.attrs[_attr])
#
#         # 不通过属性 直接查找
#         else:
#             if tag.name == ruler_pair[1]:
#                 if tag.text is not None and tag.text != '':
#                     # return (ruler_pair[0], tag.text)
#                     result = (ruler_pair[0], tag.text)
#
#         # 星判断
#         if result != None and len(result) > 1 and result[0].count('*') > 0:
#             key = ''
#             value = ''
#             value_list = []
#             if ruler_pair[0].count('*') > 0:
#                 if len(tag.contents) > 1:#多重判断
#                     for con in tag:
#                         if isinstance(con, Tag):
#                             #提取p标签
#                             if ruler_pair[0].count('***') == 1:
#                                 if con.name == 'p':
#                                     # value += con.get_text()
#                                     # value += ExtraHtml.ruler_finder_recursion_dig_for_p(con)
#                                     ExtraHtml.ruler_finder_recursion_dig_for_p(con, value_list)
#                             # 删除所有标签
#                             elif ruler_pair[0].count('**') == 1:
#                                 value += con.get_text()
#                             # 保留标签
#                             elif ruler_pair[0].count('*') == 1:
#                                 value += str(con)
#
#                 else:#单tag 判断
#                     if ruler_pair[0].count('**') == 1:
#                         value += tag.get_text()
#                     elif ruler_pair[0].count('*') == 1:
#                         value += str(tag)
#
#                 #善后
#                 if ruler_pair[0].count('***') == 1:
#                     # value = "".join(value.split())
#                     value = "".join(value_list)
#                     value = "".join(value.split())
#                     key = StringHelper.cutfrom(ruler_pair[0], '***')
#                 elif ruler_pair[0].count('**') == 1:
#                     value = "".join(value.split())
#                     key = StringHelper.cutfrom(ruler_pair[0], '**')
#                 elif ruler_pair[0].count('*') == 1:
#                     key = StringHelper.cutfrom(ruler_pair[0], '*')
#
#             elif ruler_pair[0].count('^') > 0:
#                 value = tag.text
#                 value = "".join(value.split())
#                 key = StringHelper.cutfrom(ruler_pair[0], '^')
#             else:
#                 key = ruler_pair[0]
#                 value = tag.text
#
#             if value == '':
#                 print('info: in ruler_finder_ex star filter -> ' + result[0] + ' got empty result!')
#                 value = result[1]
#
#             return (key, value)
#         elif result == None:
#             return None
#         else:
#             return result