# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import global_list


class SpiderPipeline(object):

    def __init__(self):
        self.top10 = []
        # self.comment = CommentItem()
        self.file = codecs.open('a.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        if len(self.top10) < 10:
            self.top10.append(item)
        else:
            self.top10.sort(key=lambda c: c['likeNum'])
            min_item = self.top10[0]
            if min_item['likeNum'] < item['likeNum']:
                self.top10.remove(min_item)
                self.top10.append(item)

    def close_spider(self, spider):
        self.top10.sort(key=lambda c: c['likeNum'], reverse=True)
        self.file.write("song_list_nums:".encode('utf-8') + str(global_list.song_list_num) + "\n")
        self.file.write("song_nums:".encode('utf-8') + str(global_list.song_num) + "\n")
        for a in self.top10:
            line = json.dumps(dict(a)) + "\n"
            self.file.write(line.decode("unicode_escape"))
        self.file.close()

