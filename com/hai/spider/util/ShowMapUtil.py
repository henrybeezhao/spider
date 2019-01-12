#!-*-coding:utf-8-*-
__author__ = 'zhl'

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

import MongoUtil


# 进行绘图
def showMap(dictData):
    try:
        dictData = dict(dictData)
        # 字典的大小
        length = len(dictData)
        count = 0
        for key in dictData:
            valueList = dictData.get(key)
            # 需要三个参数，第一个参数表示x轴含有多少个图，第二个参数表示y轴含有多少个图，第三个参数表示当前图处于第几个位置
            count = count + 1
            if count > length:
                break
            plt.subplot(length, 1, count)
            print(valueList[0])
            print(valueList[1])
            plt.plot(valueList[0], valueList[1], 'o-')
            plt.title(key)
            plt.xlabel('日期')
            plt.ylabel('热度')
        # 绘制图形
        plt.show()
    except Exception as  e:
        print(e)


if __name__ == "__main__":
    # 查询mongo获取数据
    source = "baidu"
    category = "hot_realtime"
    title = "奚梦瑶坐何家专车"
    mapData = MongoUtil.queryData(source, category, title)
    # 绘制图片
    showMap(mapData)
