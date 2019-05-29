import requests
import re
import time
from libs.checkproxy import CheckProxy
from libs.rabbitmq import publish_task
import json


class ProxySpider(object):

    '''89代理'''

    def __init__(self):
        self.page = 5
        self.result = []

    def get(self):
        for p in range(1, self.page+1):
            for item in self.get_one(p):
                yield item

    def get_one(self, page):
        ret = []
        r = requests.get("http://www.89ip.cn/index_{}.html".format(page))

        ret_list = re.findall(r'<td>.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?</td>.*?<td>.*?(\d+).*?</td>', r.text, re.S)

        for proxyip, proxyport in ret_list:
            ret.append((proxyip, proxyport, "http"))
        return ret


# ips_list = ProxySpider().get()
#
# for item in ips_list:
#     proxyip, proxyport, proxytype = item
#     print("[?] Test {}://{}:{} ".format(proxytype, proxyip, proxyport))
#
#     stime = time.time()
#     if CheckProxy.check(proxyip, proxyport, proxytype):
#         publish_task("ip89", json.dumps(item))
#         etime = time.time()
#         print("[*] {}://{}:{} request speed {}s..".format(proxytype, proxyip, proxyport, int(etime-stime)))
