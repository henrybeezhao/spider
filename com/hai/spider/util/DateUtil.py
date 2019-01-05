# ！-*-coding:utf-8-*-
__author__ = 'henrybee'

import datetime


# 获取当前时间，格式为
def nowSplit():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    print(nowSplit())
