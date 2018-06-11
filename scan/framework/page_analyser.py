from bs4 import BeautifulSoup
from bs4.element import Tag

from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_go import RequestHelper
from CoTec.utility.date.date_go import DateGo
from CoTec.utility.string.string_go import StringHelper


class Analyser:

    def __init__(self, first='', second='', third=''):
        self.first = first
        self.second = second
        self.third = third

        self.find_constant()

    first = ''
    second = ''
    third = ''

    part_second = []
    part_third = []

    constant_sec = ''
    constant = ''
    full_variable = ''
    variable_sec = ''
    suffix = ''
    prefix = ''

    in_index = 0
    out_index = 0

    list_sec = []
    list_thi = []

    # 1增加 0减小
    to_right = True

    def get_url(self, index):
        if index == 1:
            return self.first
        elif index == 2:
            return self.second
        elif index == 3:
            return self.third
        elif index > 3:
            return self.generate_url(index)
        else:
            return None

    """以第二页作为参考"""
    def generate_url(self,index):
        """

        :param index:
        :return:
        """
        if index <= 3:
            return None

        ref = int(self.variable_sec[0])
        dis = index - 2

        if self.to_right:
            ref += dis
        else:
            ref -= dis

        self.part_third[self.out_index] = StringHelper.exchange(self.constant_sec, self.variable_sec[0], str(ref), self.variable_sec[1])

        url = "/".join(self.part_third)
        return url

    def find_constant(self):
        self.part_second = StringHelper.url_divider(self.second)
        self.part_third = StringHelper.url_divider(self.third)

        for i in range(0,len(self.part_second)):
            if self.part_second[i] != self.part_third[i]:
                self.out_index = i
                break

        self.constant_sec = self.part_second[self.out_index]
        constant_thi = self.part_third[self.out_index]

        self.list_sec = self.find_num_ex(self.constant_sec)
        self.list_thi = self.find_num_ex(constant_thi)

        for i in range(0, len(self.list_sec)):
            if self.list_sec[i] != self.list_thi[i]:
                self.variable_sec = self.list_sec[i]
                if self.list_sec[i] < self.list_thi[i]:
                    self.to_right = True
                else:
                    self.to_right = False

    def find_num(self,str):
        num_list = []
        tar = ''
        length = 0
        flag = False
        index = 0

        for char in str:
            try:
                num = int(char)

                if flag == False:
                    index = length
                flag = True
                tar += char
            except:
                if len(tar) > 0:
                    num_list.append((int(tar),index))
                    tar = ''
                    index = 0
                    flag = False
            length += 1
        return num_list

    def find_num_ex(self,mass):
        num_list = []
        tar = ''
        length = 0
        flag = False
        index = 0

        is_num = False
        for i in range(0, len(mass)):
            try:
                num = int(mass[i])
                is_num = True
            except:
                is_num = False

            if is_num:
                num = int(mass[i])

                if flag == False:
                    index = length
                flag = True
                tar += mass[i]

            if not is_num or i == len(mass) - 1:
                if len(tar) > 0:
                    num_list.append((int(tar),index))
                    tar = ''
                    index = 0
                    flag = False

        return num_list

# extra0 = 'http://ent.163.com/special/000381Q1/newsdata_movieidx.js?callback=data_callback'
# extra1 = 'http://ent.163.com/special/000381Q1/newsdata_movieidx_02.js?callback=data_callback'
# extra2 = 'http://ent.163.com/special/000381Q1/newsdata_movieidx_03.js?callback=data_callback'
#
# analyser = Analyser(extra0, extra1, extra2)
#
# for i in range(1,100):
#     print(analyser.get_url(i))