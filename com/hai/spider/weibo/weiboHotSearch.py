#!-*-coding:utf-8-*-
__author__ = 'zhl'

import os
import sys

import bs4
import requests
from bs4 import BeautifulSoup

sys.path.append(os.getcwd() + "../..")

from util import DateUtil
from util import MongoUtil


class Top(object):

    def get_top(self, url):
        # 进行http请求，获取response
        r = requests.get(url)
        # 获取response的返回值
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        # 定义一个返回值
        resultList = []
        # 循环处理
        for child in soup.tbody.children:
            # 定义一个map，存放地址，名称和数量
            tmp = {}
            if isinstance(child, bs4.element.Tag):
                if child.span and child.a:
                    if child.select('a["href_to"]'):
                        tmp["url"] = "http://s.weibo.com" + child.a["href_to"]
                    else:
                        tmp["url"] = "http://s.weibo.com" + child.a["href"]
                    tmp["title"] = child.a.text.strip()
                    tmp["count"] = child.span.string
                    tmp["createTime"] = DateUtil.nowSplit()
                    tmp["source"] = "weibo"
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
        realtimehot.get_top("http://s.weibo.com/top/summary?cate=realtimehot")
        print("weibo hot search start at time:%s" % DateUtil.nowSplit())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
