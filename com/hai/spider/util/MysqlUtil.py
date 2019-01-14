#!-*-coding:utf-8-*-
__author__ = 'zhl'

import os
import sys

# 添加路径
sys.path.append(os.getcwd() + "../..")

from config import Config

import MySQLdb as mysql

client = mysql.connect(host=Config.mysqlHost, user=Config.mysqlUser, passwd=Config.mysqlPasswd, db=Config.mysqlDb,
                       charset='utf8', port=Config.mysqlPort)


# 读取数据
def query(sql):
    cursor = client.cursor()
    try:
        # 执行查询
        cursor.execute(sql)
        # 获取数据
        dataList = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        # 非空进行关闭
        if cursor:
            cursor.close()
    # 返回数据
    print(dataList)
