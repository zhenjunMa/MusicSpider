# -*- coding: utf-8 -*-

import scrapy
import urllib2
import requests
from bs4 import BeautifulSoup


def parse_proxy(response):
    print response


# 获取西刺代理的高匿http代理，并验证
class ProxySpider(scrapy.Spider):
    name = "proxy"

    proxies = []

    start_urls = [
        "http://www.xicidaili.com/nn/1"
    ]

    def start_requests(self):
        http_proxies = []
        https_proxies = []

        xici_urls = [
            "http://www.xicidaili.com/nn/1",
            "http://www.xicidaili.com/nn/2",
            "http://www.xicidaili.com/nn/3"
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
                mode = tds[5].text.strip()
                if desc.encode('utf-8') == "高匿":
                    if mode == "HTTPS":
                        proxy = "https://" + ip + ":" + port
                        # noinspection PyBroadException
                        try:
                            response = requests.get("https://www.baidu.com/js/bdsug.js?v=1.0.3.0", timeout=2, allow_redirects=False, proxies={"https": proxy})
                            if response.status_code == 200 and response.content.index("function") > -1:
                                https_proxies.append(proxy)
                        except Exception, e:
                            print e
                    elif mode == "HTTP":
                        proxy = "http://" + ip + ":" + port
                        # noinspection PyBroadException
                        try:
                            response = requests.get("http://www.baidu.com/js/bdsug.js?v=1.0.3.0", timeout=2, allow_redirects=False, proxies={"http": proxy})
                            if response.status_code == 200 and response.content.index("function") > -1:
                                http_proxies.append(proxy)
                        except Exception, e:
                            print e

        print https_proxies
        print http_proxies

    def parse(self, response):
        pass
    #     for idx, tr in enumerate(response.xpath('//table[@id="ip_list"]/tr')):
    #         if idx > 0:
    #             ip = tr.xpath('td').xpath('text()')[0].extract()
    #             port = tr.xpath('td').xpath('text()')[1].extract()
    #             desc = tr.xpath('td').xpath('text()')[4].extract().encode('utf-8')
    #             mode = tr.xpath('td').xpath('text()')[5].extract().encode('utf-8')
    #
    #             if desc == "高匿" and mode == "HTTP":
    #                 proxy = "http://" + ip + ":" + port
    #                 # noinspection PyBroadException
    #                 try:
    #                     resp = requests.get("http://www.baidu.com/js/bdsug.js?v=1.0.3.0", timeout=1, allow_redirects=False, proxies={"http": proxy})
    #                     if resp.status_code == 200 and resp.content.index("function") > -1:
    #                         print "success"
    #                         self.proxies.append(proxy)
    #                 except Exception:
    #                     pass
    #     for s in self.proxies:
    #         print s





