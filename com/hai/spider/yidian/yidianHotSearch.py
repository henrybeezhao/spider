#!-*-coding:utf-8-*-
__author__ = 'zhl'

import os
import sys

import requests

sys.path.append(os.getcwd() + "../..")

from util import DateUtil
from util import MongoUtil
import json


class Top(object):

    def get_top(self, url):
        # 进行http请求，获取response
        response = requests.get(url)
        # 获取response的返回值
        dataJson = json.loads(response.text)
        code = dataJson.get("code")
        if 0 == code:
            keywords = dataJson.get("keywords")
            # 定义一个返回值
            resultList = []
            # keywords结果为json，进行json处理
            count = 100
            for item in keywords:
                tmp = {}
                tmp["url"] = ""
                tmp["title"] = item.get("name")
                tmp["count"] = count
                count = count - 1
                tmp["createTime"] = DateUtil.nowSplit()
                tmp["source"] = "yidian"
                tmp["category"] = "hot_search"
                # 加入list
                resultList.append(tmp)
            # 插入mongo库
            MongoUtil.saveMongoForHotSearch(resultList)


def main():
    try:

        # 创建对象
        realtimehot = Top()
        # 进行查询
        realtimehot.get_top(
            "https://www.yidianzixun.com/home/q/hot_search_keywords?appid=web_yidian&_=%s" % DateUtil.getNowTimeMillisecond())
        print("yidian hot search start at time:%s" % DateUtil.nowSplit())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
