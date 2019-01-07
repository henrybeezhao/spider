# ！-*-coding:utf-8-*-
__author__ = 'henrybee'

import os
import sys

# 添加路径
sys.path.append(os.getcwd() + "../..")

from config import Config

import pymongo

client = pymongo.MongoClient(Config.mongoUri)


# 存储数据,content格式为：list[dict]
def saveMongoForHotSearch(content, db="spider", collection="hot_search"):
    # 获取db
    db = client[db]
    # 获取collection
    collection = db[collection]
    # 插入数据
    count = collection.insert_many(content)
    print("save mongo the insert count:%s" % count)


if __name__ == "__main__":
    saveData = []
    tmp = {}
    tmp["name"] = "hai"
    saveData.append(tmp)

    tmp = {}
    tmp["name"] = "long"
    saveData.append(tmp)

    saveMongoForHotSearch(saveData)
