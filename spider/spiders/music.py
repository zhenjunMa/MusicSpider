# -*- coding: utf-8 -*-

from spider.comment_items import CommentItem
import scrapy
import json


class CommentSpider(scrapy.Spider):
    name = "comment"
    # allowed_domains = ["music.163.com"]
    # start_urls = [
    #     "https://music.163.com/#/song?id=189312"
    # ]

    def start_requests(self):
        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_255677?csrf_token=37bdc4f8c949263c8003ab9cb140cc94'

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url,
            formdata={"params": "EwqXu+gKzBxeOxs0ipIsqrj3FrBx+9+0rVNMetFypm+wyolPofTK3OunU6ublmvwlKd/DOQBXXuQsG7plOY1Ld3M07otT0/zkMbRChueAwaw/vWt2preqSAjzL90fjcHZC5Fpu+2/G9phSJ2uNdzoL+CL+7p596lJ1+IreZ/EQ9YrGld5cf34wr8vnix2bWeswbFKU3mZhT7joxZCZb3VZteJfAo8ZaGRnBbHRwrvr0=", "encSecKey": "5179db23b4a2292422de58534d147edac80387513fa066f958f9d849af7a4718a4362e028884f6985eb109c0ef1fa9e7b42b9b8135fd169c273a275a90efbc635d829722e5308e5c05c77fb6cca3b4b62bbd5cd28058e1db0fc8c7d6f9026db0ae1f7596bf8c27fc405325fd0bb106c97d61801a096c5891b8731a70ed58b791"}
        )
        # for sel in response.xpath('//a[@class="s-fc7"]/text()'):
        #     print sel.extract()
        # item = CommentItem()
        # item['content'] = sel.xpath('//*[@id="118449431510662517622"]/div[2]/div[1]/div/a')[0].extract()
        # item['likeNum'] = sel.xpath('//div/a/text()').extract()
        # print item['content']
        # yield item

    def parse(self, response):
        jsonstr = json.loads(response.body_as_unicode())
        print str(jsonstr)
        for l in jsonstr["hotComments"]:
            item = CommentItem()
            item['content'] = l["content"].encode('utf-8')
            # item['reply'] = json.loads(jsonstr["beReplied"])
            item['likeNum'] = l["likeNum"]
            yield item
