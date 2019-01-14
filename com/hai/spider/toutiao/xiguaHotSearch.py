#!-*-coding:utf-8-*-
__author__ = 'zhl'

import json
import os
import sys

import requests

sys.path.append(os.getcwd() + "../..")

from util import MongoUtil
from util import DateUtil


class Top(object):

    def get_top(self, url):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        # 进行http请求，获取response
        r = requests.get(url, headers=headers)
        # 获取response的返回值
        resJson = r.text
        data = json.loads(resJson)

        # 创建list[{}]
        resultList = []
        # 定义一个总量
        totalCount = 100
        # 循环处理
        for word in data:
            tmp = {}
            tmp["url"] = ""
            tmp["title"] = word
            tmp["count"] = totalCount
            totalCount = totalCount - 1
            tmp["createTime"] = DateUtil.nowSplit()
            tmp["source"] = "xigua"
            tmp["category"] = "hot_search"
            # 加入列表
            resultList.append(tmp)
        # 插入mongo库
        MongoUtil.saveMongoForHotSearch(resultList)


def main():
    try:
        # 创建对象
        realtimehot = Top()
        # 进行查询
        realtimehot.get_top("https://www.ixigua.com/hot_words/")
        print("xigua hot search start at time:%s" % DateUtil.nowSplit())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
