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
        searchJson = data.get('data')
        searchData = json.loads(searchJson)

        # 创建list[{}]
        resultList = []
        # 定义一个总量
        totalCount = 100
        # 循环处理
        for word in searchData.get('search_words'):
            tmp = {}
            tmp["url"] = word.get("link")
            tmp["title"] = word.get("q")
            totalCount = totalCount - 1
            tmp["count"] = totalCount
            tmp["createTime"] = DateUtil.nowSplit()
            tmp["source"] = "toutiao"
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
        realtimehot.get_top(
            "https://is.snssdk.com/2/wap/search/extra/hot_word_list/?use_wk=1&hide_bar=1&hide_status_bar=1&background_colorkey=3&disable_web_progressView=1&enable_jump=1&is_new_ui=1&source=title&iid=56902458375&device_id=58205562141&channel=oppo-cpa&aid=13&app_name=news_article&version_code=705&version_name=7.0.5&device_platform=android&abflag=3&device_type=PBEM00&device_brand=OPPO&language=zh&os_api=27&os_version=8.1.0&openudid=7284731287f985db&manifest_version_code=705&resolution=1080*2340&dpi=480&update_version_code=70515&_rticket=1546829616083&plugin=26958&fp=crT_cW4_FrGtFlwOLlU1F2KIFzKe&format=json")
        print("toutiao hot search start at time:%s" % DateUtil.nowSplit())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
