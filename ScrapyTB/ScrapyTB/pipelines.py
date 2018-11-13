# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import requests

class ScrapytbPipeline(object):

    #
    # def process_item(self, item, spider):
    #     self.fp = open('jian.json', 'a', encoding='utf8')
    #     # 保存到文件中
    #     # 先将item转化为字典
    #     d = dict(item)
    #     data = {
    #         "info":"操作完成",
    #         "code":"200",
    #         "data":[d]
    #     }
    #     # 将字典转化为json格式的字符串
    #     string = json.dumps(data, ensure_ascii=False)
    #     self.fp.write(string + '\n')
    #     self.fp.close()
    #     return item

    return_list = []
    def process_item(self, item, spider):
        self.return_list.append(dict(item))
        while len(self.return_list) > 10:
            base_dir = os.getcwd()
            filename = os.path.join(base_dir, 'news.json')
            data = {
                "info":"操作完成",
                "code":"200",
                "data":self.return_list
            }
            with open(filename, "a", encoding='utf-8') as fp:
                line = json.dumps(data, ensure_ascii=False) + "\n"
                fp.write(line)
            print("----->>>", data)
            # url = "http://bgpy.wantupai.com/server/api/goods/import"
            url = "http://www.baidu.com"
            data_info = json.dumps(data)
            form_data = {"data":data_info}
            s = requests.post(url,data=form_data)
            self.return_list = []
            print('=============',s.text)
        return item