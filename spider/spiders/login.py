# -*- coding: utf-8 -*-
import base64

import os

from spider.comment_items import CommentItem
import scrapy
import json
from Crypto.Cipher import AES

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


class CommentSpider(scrapy.Spider):
    name = "login"
    # allowed_domains = ["music.163.com"]
    # start_urls = [
    #     "https://music.163.com/#/song?id=189312"
    # ]

    def start_requests(self):
        url = 'https://music.163.com/weapi/login?csrf_token=2a2ae058e08fd361171e6793ce30290c'

        text = {
            'username': 'mzj8812463a@163.com',
            'password': '3421492',
            'rememberLogin': 'false'
        }
        text = json.dumps(text)
        secKey = createSecretKey(16)
        encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
        encSecKey = rsaEncrypt(secKey, pubKey, modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }

        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url,
            formdata=data
            # meta={'cookiejar': 1},
        )

    def parse(self, response):
        # Cookie = response.headers.getlist('Set-Cookie')
        # print 'Cookie', Cookie
        print json.loads(response.body_as_unicode())
