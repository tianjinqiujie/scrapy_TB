# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import json
import re

import random

import requests
import scrapy
try:
    from ScrapyTB.ScrapyTB.items import QuoteItem
except ModuleNotFoundError as e:
    from ..items import *





class TaobaoSpider(scrapy.Spider):
    name = 'TaoBao'
    allowed_domains = ['taobao.com', 'tmall.com']
    start_urls = ['https://tce.alicdn.com/api/data.htm?ids=222887%2C222890%2C222889%2C222886%2C222906%2C222898%2C222907%2C222885%2C222895%2C222878%2C222908%2C222879%2C222893%2C222896%2C222918%2C222917%2C222888%2C222902%2C222880%2C222913%2C222910%2C222882%2C222883%2C222921%2C222899%2C222905%2C222881%2C222911%2C222894%2C222920%2C222914%2C222877%2C222919%2C222915%2C222922%2C222884%2C222912%2C222892%2C222900%2C222923%2C222909%2C222897%2C222891%2C222903%2C222901%2C222904%2C222916%2C222924&callback=tbh_service_cat']


    def parse(self, response):
        goods_cate_name_list = []
        text = requests.post(response.url).text
        re_text = re.compile(r'[(](.*)[)]', re.S)
        imee = (re.findall(re_text, text))
        res_list = imee[0]
        data = json.loads(res_list)
        cate_id = data.keys()
        for d in cate_id:
            list_id = data[d]
            list_value = list_id['value']
            list_list = list_value['list']
            for list_dict in list_list:
                name = list_dict.get('name')
                if name not in goods_cate_name_list:
                    goods_cate_name_list.append(name)
        for goods_cate_name in goods_cate_name_list:
            tb_url = 'https://s.taobao.com/list?q='
            join_url = tb_url + str(goods_cate_name)
            yield scrapy.Request(url=join_url, meta={"cate_name":goods_cate_name}, callback=self.parse_spider)
            print('..........')

    def parse_spider(self, response):
        print('=======',response.url)
        goods_cate_name = response.meta.get('cate_name')

        html = response.text
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)  # 商品名字
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)  # 商品价格
        goodid = re.findall(r'\"nid\"\:\".*?\"', html)  # 产品id
        nicklt = re.findall(r'\"nick\"\:\".*?\"', html)  # 店铺名
        pic_lt = re.findall(r'\"pic_url\"\:\".*?\"', html)  # 图片链接
        detail_url = re.findall(r'\"detail_url\"\:\".*?\"', html) # 商品详情url
        sold_num_lt = re.findall(r'\"view_sales\"\:\".*?\"', html)  # 销量
        for i in range(len(plt)):
            goods_price = eval(plt[i].split(':')[1])
            goods_product_id = eval(goodid[i].split(':')[1])
            goods_name = eval(tlt[i].split(':')[1])
            shop_name = eval(nicklt[i].split(':')[1])
            goods_image = eval(pic_lt[i].split(':')[1])
            goods_detail_url = eval(detail_url[i].split(':',1)[1])
            try:
                num = eval(sold_num_lt[i].split(':')[1])
                sale = re.findall(r'[\d]+', num)
                goods_sale_num = int(''.join(sale))
            except IndexError as e:
                print(goods_sale_num)

            goods_detail_url = "https:%s" %goods_detail_url

            item = {
                "goods_cate_name":goods_cate_name,  # 类名
                "goods_name":goods_name,  # 商品名字
                "goods_image":goods_image,  # 图片链接
                "goods_detail_url":goods_detail_url, # 商品详情url
                "goods_product_id":goods_product_id,  # 产品id
                "goods_price":goods_price,  # 商品价格
                "goods_sale_num":goods_sale_num,  # 销量
                "shop_name":shop_name    # 店铺名字
            }
            tmall_url = "https://dsr-rate.tmall.com/list_dsr_info.htm?itemId="
            taobao_url = "https://rate.taobao.com/detailCount.do?itemId="
            detail_url_str = str(detail_url)
            data_url = detail_url_str.split('.')[1]
            if data_url == 'tmall':
                url_data = tmall_url + goods_product_id
                yield scrapy.Request(url_data, meta={'titme':item}, callback=self.datail_spider)
            elif data_url == 'taobao':
                url_data = taobao_url + goods_product_id
                yield scrapy.Request(url_data, meta={'titme':item}, callback=self.datail_spider)


    def datail_spider(self, response):
        text = requests.post(response.url).text
        res = response.url


        tmp = res.split('.')[1]

        list_item = response.meta.get('titme')

        item = QuoteItem()
        goods_cate_name = list_item["goods_cate_name"]  # 类名
        goods_name = list_item["goods_name"]  # 商品名字
        goods_image = list_item["goods_image"]  # 图片链接
        goods_detail_url = list_item["goods_detail_url"] # 商品详情url
        goods_product_id = list_item["goods_product_id"]  # 产品id
        goods_price = list_item["goods_price"]  # 商品价格
        goods_sale_num = list_item["goods_sale_num"]  # 销量
        shop_name = list_item["shop_name"] # 店铺名

        item["goods_cate_name"] = goods_cate_name
        item["goods_name"] = goods_name
        item["goods_image"] = goods_image
        item["goods_detail_url"] = goods_detail_url
        item["goods_product_id"] = goods_product_id
        item["goods_price"] = goods_price
        item["goods_sale_num"] = goods_sale_num
        item["shop_name"] = shop_name
        list1 = ['4.8','4.9']

        if tmp == 'tmall':
            platform = 1
            total_score = re.findall(r'"gradeAvg":\d.\d',text)
            score = "".join(total_score)
            comment_num = re.findall(r'"rateTotal":[\d]+',text)
            comment = re.findall(r'[\d]+', comment_num[0])
            goods_comment_num = int("".join(comment))
            try:
                goods_total_score = score.split(':')[1]
            except IndexError as e:
                goods_total_score = random.choice(list1)
        elif tmp == 'taobao':
            platform = 2
            comment_num = re.findall(r'"count":[\d]+',text)
            comment = re.findall(r'[\d]+', comment_num[0])
            goods_comment_num = int("".join(comment))
            goods_total_score = random.choice(list1)
        item["platform"] = platform     # 来源
        item["goods_total_score"] = goods_total_score    # 评分
        item['goods_comment_num'] = goods_comment_num    # 商品评论数

        yield item