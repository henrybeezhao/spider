#!-*-coding:utf-8-*-
__author__ = 'henrybee'

import os
import sys
import time

import schedule

sys.path.append(os.getcwd())

from weibo import weiboHotSearch
from baidu import baiduHotSearch
from toutiao import toutiaoHotSearch
from yidian import yidianHotSearch
from config import Config


def job():
    print("job starting")
    weiboHotSearch.main()
    baiduHotSearch.main()
    toutiaoHotSearch.main()
    yidianHotSearch.main()


if __name__ == "__main__":
    # 10分钟执行一次
    schedule.every(Config.interval_minutes).minutes.do(job)
    # 运行
    while True:
        schedule.run_pending()
        time.sleep(60)
