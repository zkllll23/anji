# 作者: zkllll23
# 微博关键词爬虫
import os
import re  # 正则表达式提取文本
from jsonpath import jsonpath  # 解析ison数据
import requests  # 发送请求
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用


def trans_time(v_str):
    """
    转换GMT时间为标准格式
    :param v_str: GMT时间字符串
    :return: 标准时间格式字符串
    """
    gmt_format = '%a %b %d %H:%M:%S +0800 %Y'
    time_array = datetime.datetime.strptime(v_str, gmt_format)
    ret_time = time_array.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time


def get_weibo_list(v_keyword, v_max_page):
    """
    获取微博内容
    :param v_keyword:搜索关键词
    :param v_max_page:爬取最大页码数
    """
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }
    for page in range(1, v_max_page + 1):
        print("=====开始爬取第{}页微博=====".format(page))
        # 请求地址
        url = 'https://m.weibo.cn/api/container/getIndex'
        # 请求参数
        params = {
            "containerid": "100103type=1&q={}".format(v_keyword),
            "page_type": "searchall",
            "page": page
        }
        # 发送请求
        r = requests.get(url, headers=headers, params=params)
        print("请求状态:{}".format(r.status_code))
        # 解析json数据
        cards = r.json()["data"]["cards"]
        # 微博内容
        text_list = jsonpath(cards, '$..mblog.text')
        # 微博内容正则表达式数据清洗
        dr = re.compile(r'<[^>]+>', re.S)
        temp_text_list = []
        if not text_list:
            continue
        if type(text_list) == list and len(text_list) > 0:
            for text in text_list:
                temp_text = dr.sub('', text)
                print(temp_text)  # 输出内容
                temp_text_list.append(temp_text)
        # 微博创建时间
        time_list = jsonpath(cards, '$..mblog.created_at')
        time_list = [trans_time(v_str=i) for i in time_list]
        # 微博作者
        author_list = jsonpath(cards, '$..mblog.user.screen_name')
        # 微博id
        id_list = jsonpath(cards, '$..mblog.id')
        # 微博bid
        bid_list = jsonpath(cards, '$..mblog.bid')
        # 转发数
        reposts_count_list = jsonpath(cards, '$..mblog.reposts_count')
        # 评论数
        comments_count_list = jsonpath(cards, '$..mblog.comments_count')
        # 点赞数
        attitudes_count_list = jsonpath(cards, '$..mblog.attitudes_count')
        # 把列表数据保存成DataFrame数据
        df = pd.DataFrame(
            {
                '页码': [page] * len(id_list),
                '微博id': id_list,
                '微博bid': bid_list,
                '微博作者': author_list,
                '发布时间': time_list,
                '微博内容': temp_text_list,
                '转发数': reposts_count_list,
                '评论数': comments_count_list,
                '点赞数': attitudes_count_list,
            }
        )
        # 表头
        if os.path.exists(v_weibo_file):
            header = None
        else:
            header = ['页码', '微博id', '微博bid', '微博作者', '发布时间', '微博内容', '转发数', '评论数', '点赞数']
        # 保存csv文件
        df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding="utf_8_sig")


if __name__ == '__main__':
    # 爬取页码
    max_search_page = 100
    # 爬取关键词
    # search_keywords = ['装置艺术', '光装置', '交互体验', '疗愈', '沉浸感']
    search_keywords = ['沉浸感']  # 建议每次只爬一个关键词，防止反爬
    for search_keyword in search_keywords:
        # 保存文件名
        v_weibo_file = '微博清单/微博清单_{}_前{}页.csv'.format(search_keyword, max_search_page)
        print("爬取关键词:{},爬取页码:{},保存文件名:{}".format(max_search_page, search_keyword, v_weibo_file))
        # 如果csv文件存在则删除旧文件
        if os.path.exists(v_weibo_file):
            os.remove(v_weibo_file)
            print("微博清单已存在,删除了文件:{}".format(v_weibo_file))
        # 调用爬虫
        print("=====开始爬取=====")
        get_weibo_list(search_keyword, max_search_page)
        print("=====爬取结束=====")
        # 数据去重清洗
        df2 = pd.read_csv(v_weibo_file)
        # 删除重复数据
        df2.drop_duplicates(subset=['微博bid'], inplace=True, keep='first')
        # 保存文件
        df2.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')
