import logging

class Configs:
    index = 0

    # 无限执行
    infinity = False
    System_Interval = 4 * 60 * 60
    work_interval = 60 * 10
    work_sequence = [(1, 24)]
    # work_sequence = [(10, 11), (12, 14), (18, 18), (20, 22)]

    system_shutdown_flag_filename = "SSFF"

    #标志是否为测试状态
    debuging = True

    weibo_username = "xxx"
    weibo_password = "xxx"

    account_newrank_name = "xxx"
    account_newrank_pass = "xxx"

    check_table = False

    database_address = "xxx"
    database_name = "xxx"
    database_account = "xxx"
    database_pass = "xxx"

    #日志级别
    log_level = logging.INFO

    proxy_enable = True
    proxy_http_provider = 'http://www.xicidaili.com/nt/'
    proxy_https_provider = 'http://www.xicidaili.com/wn/'

    proxy_api_http = 'xxx'
    proxy_api_https = 'xxx'

    fish_data_post_url = "xxx"

    request_timeout = 7
    request_retry_times = 2

    email_host = 'smtp.live.com'

    email_username = 'xxx'
    email_password = 'xxx'
    email_master = 'xxx'
    email_target = [email_master,]

    report_interval = 48000#Hours

    five_key_online = True
    five_key = 'xxx'

    display_sql = False
    show_utf = True
    error_mail = False

    length_web = 3
    length_weibo = 3
    length_wechat = 3

    target_pool_size = 4

    target_queue_size = 2
    uploader_queue_size = 1


    __pic_part_path = ('/img', '')
    __file_path_prifix = ('xxx', '')

    newrank_cookie_file = 'config/cookie_newrank.txt'
    gsdata_cookie_file = 'config/cookie_gsdata.txt'

    @staticmethod
    def FILE_PATH_PRIFIX():
        return Configs.__file_path_prifix[Configs.index]

    @staticmethod
    def PIC_PART_PATH():
        return Configs.__pic_part_path[Configs.index]
