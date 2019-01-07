import json
import os
import random
import re
import sys
from hashlib import md5
from multiprocessing import Pool
from urllib.parse import urlencode

import requests

# 添加路径
sys.path.append(os.getcwd() + "../..")

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from config import Config


# 获取索引页内容
def get_page_index(offset, keyword):
    sample_list = list("abcdefghijklmnopqrstuvwxyz")
    pd = "".join(random.sample(sample_list, 9))
    # 构造请求参数
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '0',
        'from': 'search_tab',
        'pd': pd
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    # 请求url,  urlencode()将字典数据转为url请求
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print("the request url:%s,the response text:%s" % (url, response.text))
            return response.text
        return None
    except RequestException as err:
        print('请求页出错:%s' % err)
        return None


# 解析索引网页，获得详细页面url
def parse_page_index(html):
    # 解析json数据，转为json对象
    data = json.loads(html)
    # 判断data是否存在，存在则返回所有的键名
    if data and 'data' in data.keys():
        for item in data.get('data'):
            # 获取当前图片
            down_images(item.get("large_image_url"))
            # 提取article_url，把article_url循环取出来
            yield item.get('article_url')


# 获取详细页面内容
def get_page_detail(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as err:
        print('请求详细页出错:%s' % err)
        return None


# 解析详细页面内容
def parse_page_Detail(html, url):
    # 生成BeautifulSoup对象，使用lxml解析
    soup = BeautifulSoup(html, 'lxml')
    # 匹配标题
    title_pattern = re.compile('BASE_DATA.galleryInfo = {.*?title: (.*?),', re.S)
    # 匹配图片
    images_pattern = re.compile('BASE_DATA.galleryInfo = {.*?gallery: JSON.parse\("(.*?)"\)', re.S)
    result = re.search(images_pattern, html)
    title = re.search(title_pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        # 如果sub_images存在，返回所有键名
        if data and 'sub_images' in data.keys():
            # 获取sub_images的所有内容
            sub_images = data.get('sub_images')
            # 获取一组图，构造列表
            images = [item.get('url') for item in sub_images]
            # 下载图片，保存图片
            for image in images: down_images(image)
            return {
                'title': title.group(1),
                'url': url,
                'images': images
            }


# 下载图片
def down_images(url):
    print('正在下载图片:' + url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            sava_images(response.content)
        return None
    except RequestException as err:
        print('请求图片出错:%s' % err)
        return None


# 保存图片
def sava_images(content):
    file_pref = "/var/data/toutiao/" + Config.touTiaoSearchKey
    file_path = "{0}/{1}.{2}".format(file_pref, md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        # 如果不存在，则创建目录
        if not os.path.isdir(file_pref):
            os.mkdir(file_pref)

        with open(str(file_path), 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    # 获取索引页内容
    # 传入第一个变量为offset值，第二个为关键字，网页通过滑动，offset值会发生改变
    html = get_page_index(offset, Config.touTiaoSearchKey)
    # 解析索引页内容，获取详细页面URL
    for url in parse_page_index(html):
        if url:
            # 将详细页面内容赋值给html
            html = get_page_detail(url)
            # 如果详细页面内容不为空，则解析详细内容
            if html:
                result = parse_page_Detail(html, url)
                # print(result)


if __name__ == '__main__':
    # 执行搜索处理
    groups = [x * 20 for x in range(0, 20 + 1)]
    # 创建进程池
    pool = Pool()
    # 开启多进程
    pool.map(main, groups)
