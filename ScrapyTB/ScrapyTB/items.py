# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):

    # 判断天猫淘宝
    platform = scrapy.Field()
    # 分类名称
    goods_cate_name = scrapy.Field()
    # 商品名称
    goods_name = scrapy.Field()
    # 商品图片连接
    goods_image = scrapy.Field()
    # 详情连接
    goods_detail_url = scrapy.Field()
    # 第三方平台id
    goods_product_id = scrapy.Field()
    # 价格
    goods_price = scrapy.Field()
    # 销售量
    goods_sale_num = scrapy.Field()
    # 评分
    goods_total_score = scrapy.Field()
    # 店铺名字
    shop_name = scrapy.Field()
    # 商品品论数
    goods_comment_num = scrapy.Field()