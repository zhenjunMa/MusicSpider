# -*- coding: utf-8 -*-


# 由于不会python，用来做测试
import requests


class A:

    category = ["华语", "欧美", "日语", "韩语", "粤语", "小语种"]

    def __init__(self):
        pass

    if __name__ == '__main__':
        # for s in category:
        #     print s
        print requests.get("http://www.xicidaili.com/nn/1")
