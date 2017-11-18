# -*- coding: utf-8 -*-

from spider.comment_items import CommentItem
import scrapy
import json


domain_link = 'https://music.163.com'
comment_link = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_'

limit = 35


# 解析歌曲页
def parse_song_page(response, song_id, song_name):
    jsonstr = json.loads(response.body_as_unicode())
    if len(jsonstr["hotComments"]) > 0:
        item = CommentItem()
        item['id'] = song_id
        item['name'] = song_name
        item['content'] = jsonstr["hotComments"][0]["content"].encode('utf-8')
        # item['reply'] = json.loads(jsonstr["beReplied"])
        item['likeNum'] = jsonstr["hotComments"][0]["likedCount"]
        yield item


# 解析歌单列表页
def parse_song_list_page(response):
    for l in response.xpath('//ul[@class="f-hide"]/li/a'):
        song_name = l.xpath("text()")[0].extract()
        song_id = l.xpath('@href')[0].extract().split("=")[1]

        yield scrapy.FormRequest(
            comment_link + song_id + "?csrf_token=",
            formdata={"params": "xk/7lCFhrKKRmp33SBs87Yx6/9YwEHKRYlwsW5TVVn2jJ+832PNKWa798LraAwXO7hd/RD+eVZgLFnKHntbTqY52J5RTteZnYKwD1lCJnpX9x8RPeoESWo0PJ0/RPD+HxI5u3baQD4DLMOQU5DJ+0uiRcsckvxkFW8U4MAjkFWI2yN0SvrJetTERoaqU20up", "encSecKey": "8f43f3aaaa9a6e1060f04486b7c42619ab9543aca4000b885469afe992d4c86423c6bfe3494d71dcfab426891a0177347a089dd5b19561fd93ac7b79f7b617ec2b13ac677d709c2a22fb68521a181c737711e1d4cb294cb466faa40c9ca687d43d71e4e2eeaad5a217bcb01e121ae6229d5d05f129d8f91a51997fa8712df5a0"},
            callback=lambda arg1=response, arg2=song_id, arg3=song_name: parse_song_page(arg1, arg2, arg3)
        )


# 解析歌单页
def parse_list_page(response):
    for music_list in response.xpath('//a[@class="tit f-thide s-fc0"]'):
        music_list_name = music_list.xpath('text()')[0].extract()
        music_list_suffix = music_list.xpath('@href')[0].extract()
        print music_list_name.encode("utf-8")
        yield scrapy.Request(domain_link + music_list_suffix, callback=parse_song_list_page)


class PlayListSpider(scrapy.Spider):
    name = "most_like_comment"
    allowed_domains = ["music.163.com"]

    category = ["华语", "欧美", "日语", "韩语", "粤语", "小语种"]

    start_urls = [
        # "https://music.163.com/discover/playlist"
        "https://music.163.com/discover/playlist?order=hot&cat=华语"
    ]

    def parse(self, response):
        max_page_num = int(response.xpath('//a[@class="zpgi"]')[len(response.xpath('//a[@class="zpgi"]')) - 1].xpath('text()')[0].extract())
        for i in range(0, max_page_num):
            offset = i * limit
            music_list_link = "https://music.163.com/discover/playlist?order=hot&cat=华语&limit=" + str(limit) + "&offset=" + str(offset)
            yield scrapy.Request(music_list_link, callback=parse_list_page)



