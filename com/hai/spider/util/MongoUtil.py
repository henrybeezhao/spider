# ！-*-coding:utf-8-*-
__author__ = 'henrybee'

import os
import sys

# 添加路径
sys.path.append(os.getcwd() + "../..")

from config import Config

import pymongo
import json

client = pymongo.MongoClient(Config.mongoUri)


# 存储数据,content格式为：list[dict]
def saveMongoForHotSearch(content, db="spider", collection="hot_search"):
    # 获取db
    db = client[db]
    # 获取collection
    collection = db[collection]
    # 插入数据
    collection.insert_many(content)


# 从数据库查询数据，返回的数据格式为：[{title:[[],[]]}]
def queryData(source, category, title, db="spider", collection="hot_search"):
    # 获取db
    db = client[db]
    # 获取collection
    collection = db[collection]
    # 构造查询条件
    query = {}
    if source:
        query["source"] = source
    if category:
        query["category"] = category
    if title:
        query["title"] = title
    # 获取数据
    result = collection.find(query, {"_id": 0}).sort("{createTime:-1}")
    # 定义字典
    tmpDict = {}
    for i in result:
        dd = json.dumps(i)
        data = json.loads(dd)
        # 获取值
        title = data.get("title")
        count = data.get("count")
        createTime = data.get("createTime").replace("-", "").replace(" ", "").replace(":", "")[6:12]
        # title已经存在
        if title in tmpDict.keys():
            valueList = tmpDict.get(title)
            xList = valueList[0]
            yList = valueList[1]
            # 添加当前值
            xList.append(createTime)
            yList.append(count)
            # 加入list
            valueList[0] = xList
            valueList[1] = yList
            # 重新设置
        else:
            valueList = []
            xList = [createTime]
            yList = [count]
            # 加入list
            valueList.append(xList)
            valueList.append(yList)
        # 设置tmp
        tmpDict[title] = valueList
    # 返回结果
    return tmpDict


if __name__ == "__main__":
    print(queryData("baidu", "hot_today", "李诞吐槽张艺兴"))
