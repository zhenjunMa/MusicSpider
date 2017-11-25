# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random

import requests
import urllib2
import logging
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf8")


class RotateUserAgentMiddleware(object):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]


http_proxies = []


def get_new_proxies():
    xici_urls = [
        "http://www.xicidaili.com/nn/1",
        "http://www.xicidaili.com/nn/2",
        "http://www.xicidaili.com/nn/3",
        "http://www.xicidaili.com/nn/4",
    ]
    for url in xici_urls:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        referer = 'http://www.zhihu.com/articles'
        headers = {"User-Agent": user_agent, 'Referer': referer}
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response.read())
        table = soup.find("table", attrs={"id": "ip_list"})
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[1].text
            port = tds[2].text
            desc = tds[4].text
            if desc.encode('utf-8') == "高匿":
                proxy = "http://" + ip + ":" + port
                # noinspection PyBroadException
                try:
                    response = requests.get("http://www.baidu.com/js/bdsug.js?v=1.0.3.0", timeout=1, allow_redirects=False, proxies={"http": proxy})
                    if response.status_code == 200 and response.content.index("function") > -1:
                        http_proxies.append(proxy)
                except Exception, e:
                    logging.info("验证代理IP异常：" + str(e))


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        if "music.163.com" in request.url:
            # 需要更换代理
            if "change_proxy" in request.meta.keys():
                del request.meta['change_proxy']
                # 删除无用代理
                invalid_proxy = request.meta['proxy']
                if invalid_proxy in http_proxies:
                    http_proxies.remove(invalid_proxy)

            # 没有可用代理，需要重新从西刺代理获取
            while len(http_proxies) == 0:
                logging.info("没有可用代理，开始重新获取...")
                get_new_proxies()
                logging.info("本次获取到有效代理IP：" + str(http_proxies))

            proxy = random.choice(http_proxies)
            request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        if "music.163.com" in request.url:
            try:
                jsonstr = json.loads(response.body_as_unicode())
                if "msg" in jsonstr.keys():
                    if jsonstr['msg'] == 'Cheating':
                        # 请求被封则换代理重试
                        logging.info("IP被封，开始重新获取..." + request.meta['proxy'])
                        request.meta['change_proxy'] = True
                        request.dont_filter = True
                        return request
            except Exception:
                pass

        return response

    def process_exception(self, request, exception, spider):
        if "music.163.com" in request.url:
            logging.error("爬取网易云音乐异常，url=" + str(request.url) + "，异常：" + str(exception))
            # 异常重新处理
            request.dont_filter = True
            return request


