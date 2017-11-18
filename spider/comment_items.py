# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    id = scrapy.Field()        # 歌曲ID
    name = scrapy.Field()      # 歌曲名
    content = scrapy.Field()   # 评论内容
    reply = scrapy.Field()     # 回复内容
    likeNum = scrapy.Field()   # 点赞数