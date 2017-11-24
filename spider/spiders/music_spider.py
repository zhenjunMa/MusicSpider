# -*- coding: utf-8 -*-

import json

import scrapy

from spider import global_list
from spider.comment_items import CommentItem

domain_link = 'https://music.163.com'
comment_link = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_'

limit = 35


# 解析歌曲页
def parse_song_page(response):
    global_list.song_num += + 1
    song_name = response.meta['song_name']
    song_id = response.meta['song_id']
    jsonstr = json.loads(response.body_as_unicode())
    if len(jsonstr["hotComments"]) > 0:
        for comm in jsonstr["hotComments"]:
            item = CommentItem()
            item['song_id'] = song_id
            item['song_name'] = song_name
            item['content'] = comm["content"]
            # item['reply'] = json.loads(jsonstr["beReplied"])
            item['likeNum'] = comm["likedCount"]
            yield item


# 解析歌单列表页
def parse_song_list_page(response):
    global_list.song_list_num += + 1
    for l in response.xpath('//ul[@class="f-hide"]/li/a'):
        song_name = l.xpath("text()")[0].extract()
        song_id = l.xpath('@href')[0].extract().split("=")[1]

        yield scrapy.FormRequest(
            comment_link + song_id + "?csrf_token=",
            formdata={"params": "xk/7lCFhrKKRmp33SBs87Yx6/9YwEHKRYlwsW5TVVn2jJ+832PNKWa798LraAwXO7hd/RD+eVZgLFnKHntbTqY52J5RTteZnYKwD1lCJnpX9x8RPeoESWo0PJ0/RPD+HxI5u3baQD4DLMOQU5DJ+0uiRcsckvxkFW8U4MAjkFWI2yN0SvrJetTERoaqU20up", "encSecKey": "8f43f3aaaa9a6e1060f04486b7c42619ab9543aca4000b885469afe992d4c86423c6bfe3494d71dcfab426891a0177347a089dd5b19561fd93ac7b79f7b617ec2b13ac677d709c2a22fb68521a181c737711e1d4cb294cb466faa40c9ca687d43d71e4e2eeaad5a217bcb01e121ae6229d5d05f129d8f91a51997fa8712df5a0"},
            callback=parse_song_page,
            meta={"song_name": song_name, "song_id": song_id}
        )


# 解析歌单页
def parse_list_page(response):
    for music_list in response.xpath('//a[@class="tit f-thide s-fc0"]'):
        # music_list_name = music_list.xpath('text()')[0].extract()
        music_list_suffix = music_list.xpath('@href')[0].extract()
        # print music_list_name.encode("utf-8")
        yield scrapy.Request(domain_link + music_list_suffix, callback=parse_song_list_page)


# 全网易云音乐点赞最多评论爬虫
class MusicSpider(scrapy.Spider):
    name = "music_spider"
    allowed_domains = ["music.163.com"]

    category = ["华语", "欧美", "日语", "韩语", "粤语", "小语种"]

    main_url = "https://music.163.com/discover/playlist?order=hot&cat="

    def start_requests(self):
        for cat in self.category:
            yield scrapy.Request(self.main_url + cat)

    def parse(self, response):
        cat = response.url.split("cat=")[1]
        max_page_num = int(response.xpath('//a[@class="zpgi"]')[len(response.xpath('//a[@class="zpgi"]')) - 1].xpath('text()')[0].extract())
        for i in range(0, max_page_num):
            offset = i * limit
            music_list_link = "https://music.163.com/discover/playlist?order=hot&cat=" + cat + "&limit=" + str(limit) + "&offset=" + str(offset)
            yield scrapy.Request(music_list_link, callback=parse_list_page)


