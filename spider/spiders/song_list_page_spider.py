# -*- coding: utf-8 -*-

import scrapy

from spider.spiders.playlist import parse_song_list_page


# 获取指定歌单页的所有歌曲中点赞最多的前10条评论
class SongListPageSpider(scrapy.Spider):
    name = "song_list_page"
    song_list_id = "1985399911"

    start_urls = [
        "https://music.163.com/playlist?id=" + song_list_id
    ]

    def parse(self, response):
        return parse_song_list_page(response)
