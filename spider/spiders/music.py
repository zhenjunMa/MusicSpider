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
        url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_255677?csrf_token='

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url,
            formdata={"params": "xk/7lCFhrKKRmp33SBs87Yx6/9YwEHKRYlwsW5TVVn2jJ+832PNKWa798LraAwXO7hd/RD+eVZgLFnKHntbTqY52J5RTteZnYKwD1lCJnpX9x8RPeoESWo0PJ0/RPD+HxI5u3baQD4DLMOQU5DJ+0uiRcsckvxkFW8U4MAjkFWI2yN0SvrJetTERoaqU20up", "encSecKey": "8f43f3aaaa9a6e1060f04486b7c42619ab9543aca4000b885469afe992d4c86423c6bfe3494d71dcfab426891a0177347a089dd5b19561fd93ac7b79f7b617ec2b13ac677d709c2a22fb68521a181c737711e1d4cb294cb466faa40c9ca687d43d71e4e2eeaad5a217bcb01e121ae6229d5d05f129d8f91a51997fa8712df5a0"}
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
            item['reply'] = json.loads(jsonstr["beReplied"])
            item['likeNum'] = l["likedCount"]
            yield item
