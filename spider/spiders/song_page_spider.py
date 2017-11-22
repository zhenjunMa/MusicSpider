# -*- coding: utf-8 -*-

import scrapy

from spider.spiders.playlist import parse_song_page


# 根据指定song_id获取歌曲详情页中热门评论的第一条，即点赞数最多的一条。
# song_name可以不指定
class SongPageSpider(scrapy.Spider):
    name = "song_page"
    song_id = "255677"
    song_name = ""

    def start_requests(self):
        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + self.song_id + '?csrf_token=37bdc4f8c949263c8003ab9cb140cc94'

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url,
            formdata={"params": "EwqXu+gKzBxeOxs0ipIsqrj3FrBx+9+0rVNMetFypm+wyolPofTK3OunU6ublmvwlKd/DOQBXXuQsG7plOY1Ld3M07otT0/zkMbRChueAwaw/vWt2preqSAjzL90fjcHZC5Fpu+2/G9phSJ2uNdzoL+CL+7p596lJ1+IreZ/EQ9YrGld5cf34wr8vnix2bWeswbFKU3mZhT7joxZCZb3VZteJfAo8ZaGRnBbHRwrvr0=", "encSecKey": "5179db23b4a2292422de58534d147edac80387513fa066f958f9d849af7a4718a4362e028884f6985eb109c0ef1fa9e7b42b9b8135fd169c273a275a90efbc635d829722e5308e5c05c77fb6cca3b4b62bbd5cd28058e1db0fc8c7d6f9026db0ae1f7596bf8c27fc405325fd0bb106c97d61801a096c5891b8731a70ed58b791"}
        )

    def parse(self, response):
        return parse_song_page(response, self.song_id, self.song_name)