# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo, scrapy
from scrapy.pipelines.images import ImagesPipeline


# 存储到MongoDB
class ErshouchePipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        self.db[collection_name].insert(dict(item))
        return item


class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):  # 下载图片
        for image_url in item['车辆图集']:
            yield scrapy.Request(image_url,meta={'item': item, 'index': item['车辆图集'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']  # 通过上面的index传递过来列表中当前下载图片的下标
        # 图片文件名
        image_name = re.sub('/', '', request.url) + '.jpg'
        # 图片下载目录
        filename = '/Users/xiaolongxia/Desktop/11/{0}/{1}'.format(item['车辆名称'], image_name)
        return filename