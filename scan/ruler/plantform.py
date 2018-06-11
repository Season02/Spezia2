import datetime

from CoTec.core.exception.exception_go import *
from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_go import RequestHelper

from CoTec.utility.string.string_go import StringHelper as s

from ...scan.dao.DBStructure import *
from ...scan.dao.program_dao import ProgramDao
from ...scan.dao.soap_dao import SoapDao

from ...scan.framework.html_scraper import ExtraHtml
from ...scan.framework.json_scraper import ExtraJSON
from ...scan.entity.Target import Target

from Spezia2.config.global_var import Configs

from ..ruler.BaseRuler import BaseRuler


class Plantform(BaseRuler):
    req = RequestHelper()

    mgtv_base  = 'http://vc.mgtv.com/v2/dynamicinfo?cid={0}'
    sohu_base  = 'http://count.vrs.sohu.com/count/query_Album.action?albumId={0}'
    qq_base    = 'https://m.v.qq.com/play.html?cid={0}'
    letv_base  = 'http://v.stat.letv.com/vplay/queryMmsTotalPCount?pid={0}&vid={1}'
    iqiyi_base = 'http://mixer.video.iqiyi.com/jp/albums/{0}'
    cntv_base  = 'http://www.soku.com/detail/show/{0}'
    youku_base = 'http://list.youku.com/show/{0}.html'

    youku_prefix = 'id_{0}'

    """
    优酷采用 电脑版 节目简介页 地址 例如 http://list.youku.com/show/id_z0f2233c722ec11e6bdbb.html 或者 地址中的 id id_z0f2233c722ec11e6bdbb 或者精简后的 z0f2233c722ec11e6bdbb
    芒果tv 采集于 电脑版地址 封面页 id 例如 http://www.mgtv.com/h/295541.html?fpa=se 中的 295541
    腾讯采用 应该是 节目简介页 链接地址中的 字母数字混合id 于 PC版 但是抓取用的可能是移动版 例如 https://v.qq.com/x/cover/dhzimk1qzznf301/l0024si3r7q.html 中的 dhzimk1qzznf301 或者 http://v.qq.com/detail/4/45yhivg8n755kh1.html 中的 45yhivg8n755kh1
    爱奇艺使用 id 于 移动版开发模式 找一个像id 的 (另外，我发现电影话是 tvId 或者 aId 或者 referenceId 或者 albumId 电影的话有些不好找 是在一个 content_config 开头的请求里) 例如 http://m.iqiyi.com/v_19rrax9nq4.html#vfrm=13-0-0-1 中的 204446001?callback=Zepto1499852260800 中的 204446001
    搜狐采用 pid 或者 albumId(可能是电影才用) 于 移动版地址栏中的数字 如 http://m.film.sohu.com/album/9344732.html 中的 9344732 或者 PC详情页 开发模式 例如 http://tv.sohu.com/s2017/dnwshylxt/ 中的 v?id=3879082&pid=9347799&pageNum=1&pageSize=50&isgbk=true&var=video_similar_search_result 中的 pid 9347799
    乐视采用 pid 和 vid 于 移动版播放页开发模式 例如 http://m.le.com/vplay_29037420.html 中的 queryMmsTotalPCount?pid=10036184&vid=29037420&rnd=1499915428741&callback=jsonp4 中的 pid 和 vid
    cntv采用 优酷 搜酷平台获取播放量 使用地址id 于简介页 例如 http://www.soku.com/detail/show/XMTI1NDY1Ng 中的 XMTI1NDY1Ng
    """

    # @Annoations.exe_time
    def scan(self, target, order):
        result = []

        type = self.td(target)
        url = target.extra0#'http://ent.people.com.cn/GB/81374/index1.html'

        cap = None
        ruler = None

        if self.td(target) == 'i':
            cap = ['var tvInfoJs=', '']
            url = self.iqiyi_base.format(url)
            ruler = 'keywords:contentKeyword;latestOrder:latestOrder;name:name;playCount:playCount;score:score;videoCount:videoCount'

        elif type == 'l':
            ruler = 'score:plist_score;comments:pcommon_count;bullets:pdm_count;like:up;hate:down;playCount:plist_play_count'
            url = self.letv_base.format(url, target.extra1)

        elif type == 't':
            cap = ["tlux.dispatch('$cover',", ");"]
            ruler = 'score:score->score;playCount:view_all_count;videoCount:episode_all;latestOrder:episode_updatedd'
            url = self.qq_base.format(url)

        elif type == 'm':
            url = self.mgtv_base.format(url)
            cap = ['"data":', ',"msg"']
            ruler = 'playCount:all;like:like;hate:unlike'

        elif type == 'y':
            ruler = 'playCount:li [总播放数];comments:li [评论];like:li [顶];score:span class=star-num'
            if not s.is_url(url):
                if not url.startswith('id'):
                    url = self.youku_prefix.format(url)
                url = self.youku_base.format(url)

        elif type == 's':
            url = self.sohu_base.format(url)

        elif type == 'c':
            url = self.cntv_base.format(url)
            ruler = 'playCount:^label [播放次数]'

        try:
            encode = ExtraHtml.get_page_encode(url)

            if type == 'y' or type == 'c':
                result = self.looper_html(url, ruler, encode, target)
            else:
                raw = RequestHelper.get(url, encode=encode)

                if type == 's':
                    result = self.finder_sohu(raw)
                else:
                    result = self.looper_js(raw, ruler, cap)
        except AttributeError as e:
            pass
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            print(msg)
            LogGo.warning(repr(e))

        if len(result) > 0:
            result = self.build_base_dic(target, result, order)

        return result[0]

    def union(self):
        """整合"""
        result = []
        soap = SoapDao()
        list = soap.get_new_count()

        pro_list = []

        while len(list) > 0:
            soap = list.pop(0)
            tmp_list = [soap]
            for i in range(len(list)-1, -1, -1):
                if list[i][TBSoap.program.key] == soap[TBSoap.program.key]:
                    tmp_list.append(list.pop(i))
            pro_list.append(tmp_list)

        if len(pro_list) > 0:
            result = self.build_count_dic(pro_list)

        return result

    def looper_js(self, raw, ruler, cap):
        # iqiyi_cap = ['var tvInfoJs=', '']
        # cap = Sh.str_to_tup(extra3_tup)
        list = ExtraJSON.extra_any_json_dic(raw, ruler, cap=cap)

        return list

    def td(self, type):
        if isinstance(type, str):
            type = type
        elif isinstance(type, Target):
            type = type.soap_type

        if type == 'iqiyi' or type == 'i':
            return 'i'
        elif type == 'letv' or type == 'l':
            return 'l'
        elif type == 'qq' or type == 'q' or type == 't':
            return 't'
        elif type == 'mgtv' or type == 'm':
            return 'm'
        elif type == 'youku' or type == 'y':
            return 'y'
        elif type == 'sohu' or type == 's':
            return 's'
        elif type == 'cnty' or type == 'c':
            return 'c'
        else:
            return None

    def finder_sohu(self, raw):
        try:
            count = s.cut_tail(raw.split('=')[1], ';')

            return {'playCount':count}
        except:pass

    def looper_html(self, url, ruler, encode, target):
        content = ExtraHtml.web_extra_content(url, ruler, encode)

        if self.td(target) == 'y':
            try:
                content['comments'] = int(''.join(content['comments'].split('：')[1].split(',')))
                content['like'] = int(''.join(content['like'].split('：')[1].split(',')))
                content['playCount'] = int(''.join(content['playCount'].split('：')[1].split(',')))
            except:pass
        elif self.td(target) == 'c':
            try:
                content['playCount'] = int(''.join(content['playCount'].split(',')))
            except:pass

            # try:
            #     content['score'] = int(content['score'])
            # except:pass

        return content

    def build_base_dic(self, target, result, order):
        soap = TBSoap()
        program_dao = ProgramDao()
        soap_result = []

        try:

            name = ''
            if Configs.show_utf:
                try:
                    name = target.data_key
                except:
                    name = '<<error>>'

            LogGo.info(">>> name: " + str(name) + "(" + str(result['playCount']) + ")")

            """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
            dic = dict()

            try:
                dic[soap.play_count.key] = result['playCount']#瞬时播放量
            except KeyError as e:
                raise BaseDateLackException(str(e))

            try:
                dic[soap.keywords.key] = result['keywords']  # 关键字
            except:
                pass

            try:
                dic[soap.bullet_count.key] = result['bullets']  # 弹幕量
            except:
                pass

            try:
                dic[soap.hate_count.key] = result['hate']  # 怒踩量
            except:
                pass

            try:
                dic[soap.like_count.key] = result['like']  # 点赞量
            except:
                pass

            try:
                dic[soap.latest_order.key] = result['latestOrder']  # 最新剧集
            except:
                pass

            try:
                dic[soap.name.key] = result['name']  # 剧名
            except:
                pass

            try:
                dic[soap.name.key] = program_dao.get_title_by_id(target.program_id)
            except:
                pass

            try:
                dic[soap.score.key] = result['score']  # 分数
            except:
                pass

            try:
                dic[soap.video_count.key] = result['videoCount']  # 视频数量
            except:
                pass

            try:
                # pass
                dic[soap.program.key] = target.program_id  # program
                dic[soap.target.key] = target.id  # program
            except:
                pass

            dic[soap.plantform.key] = target.soap_type

            order += 1
            dic[soap.order_code.key] = order  # """排序代码"""
            dic[soap.create_date.key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # """此条记录创建时间"""
            dic[soap.valid.key] = 1

            soap_result.append(dic)
        except BaseDateLackException as e:
            msg = "Lake improtant data(" + str(e) + ')'
            LogGo.warning(msg)
        except DataFormatException as e:
            pass
            # msg = "Date format error: " + i['link'] + '\r\n' + str(e)
            # LogGo.warning(msg)
        except KeyError as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

        return soap_result

    def build_count_dic(self, pro_list):
        # pc = TBProgramPlayCount
        result = []

        try:

            LogGo.info(">>> count: " + str(len(pro_list)))

            for programs in pro_list:

                """字典的 键 对应数据库中的字段名 值 对应要存储的值"""
                dic = dict()

                total = 0

                for program in programs:
                    try:
                        dic[TBProgramPlayCount.program.key] = program[TBSoap.program.key]
                        plantform = program[TBSoap.plantform.key]
                        count = program[TBSoap.play_count.key]

                        total += count

                        if self.td(plantform) == 'i':
                            dic[TBProgramPlayCount.count1.key] = count
                        elif self.td(plantform) == 'l':
                            dic[TBProgramPlayCount.count2.key] = count
                        elif self.td(plantform) == 't':
                            dic[TBProgramPlayCount.count3.key] = count
                        elif self.td(plantform) == 'm':
                            dic[TBProgramPlayCount.count4.key] = count
                        elif self.td(plantform) == 'y':
                            dic[TBProgramPlayCount.count5.key] = count
                        elif self.td(plantform) == 's':
                            dic[TBProgramPlayCount.count6.key] = count
                    except Exception as e:
                        import traceback
                        msg = traceback.format_exc()
                        LogGo.info(msg)

                dic[TBProgramPlayCount.total_count.key] = total
                dic[TBProgramPlayCount.create_time.key] = datetime.datetime.now().strftime('%Y-%m-%d')  # """此条记录创建时间"""

                result.append(dic)
        except BaseDateLackException as e:
            msg = "Lake improtant data(" + str(e) + ')'
            LogGo.warning(msg)
        except DataFormatException as e:
            pass
            # msg = "Date format error: " + i['link'] + '\r\n' + str(e)
            # LogGo.warning(msg)
        except KeyError as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.warning(msg)

        return result

