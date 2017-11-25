# -*- coding: utf-8 -*-
import logging

from twisted.internet import task

from scrapy.exceptions import NotConfigured
from scrapy import signals
import global_list
import sys
reload(sys)
sys.setdefaultencoding("utf8")


# 每分钟打印一次已经爬取的歌单数以及歌曲数
class ProgressStats(object):

    def __init__(self, stats, interval=60.0):
        self.stats = stats
        self.interval = interval
        self.multiplier = 60.0 / self.interval
        self.task = None

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, interval)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        self.task = task.LoopingCall(self.log, spider)
        self.task.start(self.interval)

    def log(self, spider):
        logging.info("已经爬取歌单数：" + str(global_list.song_list_num) + "，已经爬取歌曲数：" + str(global_list.song_num))

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.task.stop()
