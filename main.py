import os
import time

import sys
sys.path.append("../")

from CoTec.core.SMTP.smtp_go import SMTPServer
from CoTec.core.log.log_go import LogGo
from CoTec.core.request.request_go import RequestHelper
from CoTec.utility.file.file_go import FileHelper
from CoTec.utility.download.dl import Download

from Spezia2.scan.strategy.BaseStrategy import BaseStrategy
from Spezia2.scan.scanner import Scanner
from Spezia2.config.global_var import Configs

from CoTec.core.request.proxy_go import ProxyHelper
from CoTec.core.database.mysql_go import MysqlHelper

from CoTec.core.request.request_class_ver import RequestHelperClassVer

from Spezia2.scan.etc.somebody_help import somebody_help

def base_init():
    LogGo.init(Configs())
    RequestHelper.init(Configs())
    SMTPServer.init(Configs())
    Download(Configs())

    RequestHelperClassVer.init(Configs())
    ProxyHelper.init(Configs())
    MysqlHelper.init(Configs())
    BaseStrategy.init()

""" 程序入口 """
if __name__ == "__main__":
    base_init()

    LogGo.info('PID: ' + str(os.getpid()))
    FileHelper.record_pid(str(os.getpid()))
    LogGo.info("-- Xenoblade Online --")
    print(" ")
    print("---------Xenoblade v0.2(Super Beta Version)-----------")
    print(" ")
    print("dependencies:")
    print("APScheduler==3.3.1\r\n"
          "beautifulsoup4==4.5.3\r\n"
          "bosonnlp==0.8.0\r\n"
          "click==6.7\r\n"
          "crypto==1.4.1\r\n"
          "demjson==2.2.4\r\n"
          "Flask==0.12\r\n"
          "HTMLParser==0.0.2\r\n"
          "httplib2==0.10.3\r\n"
          "itsdangerous==0.24\r\n"
          "Jinja2==2.9.5\r\n"
          "lxml==3.7.3\r\n"
          "MarkupSafe==0.23\r\n"
          "Naked==0.1.31\r\n"
          "olefile==0.44\r\n"
          "Pillow==4.1.0\r\n"
          "PyMySQL==0.7.9\r\n"
          "PySocks==1.6.8\r\n"
          "pytz==2016.10\r\n"
          "PyYAML==3.12\r\n"
          "qcloudapi-sdk-python==2.0.9\r\n"
          "requests==2.12.4\r\n"
          "shellescape==3.4.1\r\n"
          "six==1.10.0\r\n"
          "stem==1.6.0\r\n"
          "tzlocal==1.3\r\n"
          "Werkzeug==0.11.15\r\n")
    print(" ")
    print("------ ----   --- ---getIndexNumber--- ------   ---- --")
    print(" ")

    scan = Scanner()

    while True:
        LogGo.info(">>> New Loop -->")

        try:
            scan.start()
        except Exception as e:
            import traceback
            msg = traceback.format_exc()
            LogGo.error(msg)

        if Configs.infinity:
            while not somebody_help.isthataworkday(Configs().work_sequence):
                time.sleep(60 * 60)
        else:
            break

    LogGo.info("-- GH Offline --")
    print("---------------------------------------------")
