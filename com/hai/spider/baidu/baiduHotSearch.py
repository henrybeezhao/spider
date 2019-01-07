#!-*-coding:utf-8-*-
__author__ = 'zhl'

import os
import re
import sys

import bs4
import requests
from bs4 import BeautifulSoup

sys.path.append(os.getcwd() + "../..")

from util import DateUtil
from util import MongoUtil


class Top(object):

    def get_top(self, url, category):
        # 进行http请求，获取response
        r = requests.get(url)
        r.encoding = 'gb18030'
        # 获取response的返回值
        html = r.text
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        # 定义一个返回值
        resultList = []
        # 循环处理
        for child in soup.table.children:
            # 定义一个map，存放地址，名称和数量
            tmp = {}
            if isinstance(child, bs4.element.Tag):
                if child.span and child.a:
                    if child.select('a["class~=list-title"]'):
                        tmp["url"] = child.a["href"]
                    tmp["title"] = child.a.text.strip()
                    if child.select('span["class^=icon-"]'):
                        span = child.select('span["class^=icon-"]')[0].string
                        tmp["count"] = re.search("(\d+)", span).group(0)
                    tmp["createTime"] = DateUtil.nowSplit()
                    tmp["source"] = "baidu"
                    tmp["category"] = category
                    # 加入list
                    resultList.append(tmp)

        # 插入mongo库
        MongoUtil.saveMongoForHotSearch(resultList)


def main():
    # 创建对象
    realtimehot = Top()
    # 实时热点
    realtimehot.get_top("http://top.baidu.com/buzz?b=1&fr=topbuzz_b11", "hot_realtime")
    # 今日热点
    realtimehot.get_top("http://top.baidu.com/buzz?b=341&c=513&fr=topbuzz_b341_c513", "hot_today")
    # 民生热点
    realtimehot.get_top("http://top.baidu.com/buzz?b=342&c=513&fr=topbuzz_b341_c513", "hot_livelihood")
    # 娱乐热点
    realtimehot.get_top("http://top.baidu.com/buzz?b=344&c=513&fr=topbuzz_b342_c513", "hot_entertainment")
    print("baidu hot search start at time:%s" % DateUtil.nowSplit)


if __name__ == '__main__':
    main()
