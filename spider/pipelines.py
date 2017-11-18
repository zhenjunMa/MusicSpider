# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json

from scrapy.exceptions import DropItem

from spider.comment_items import CommentItem


class SpiderPipeline(object):

    def __init__(self):
        self.likeNum = 0
        self.comment = CommentItem()
        self.file = codecs.open('a.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if item['likeNum'] > self.likeNum:
            self.likeNum = item['likeNum']
            self.comment['id'] = item['id']
            self.comment['name'] = item['name']
            self.comment['content'] = item['content']
            self.comment['likeNum'] = item['likeNum']

    def close_spider(self, spider):
        line = json.dumps(dict(self.comment)) + "\n"
        self.file.write(line.decode("unicode_escape"))


# class SpiderPipeline(object):
#
#     def __init__(self):
#         self.likeNum = 0
#         self.file = codecs.open('a.json', 'wb', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         if item['likeNum'] > self.likeNum:
#             print str(item['likeNum']) + '--------------' + str(self.likeNum)
#             self.likeNum = item['likeNum']
#             # line = json.dumps(dict(item)) + "\n"
#             # self.file.write(line.decode("unicode_escape"))
#             # else:
#             #     raise DropItem('drop')
