import requests
import re
import time
from ProxySpider.libs.checkproxy import CheckProxy


class ProxySpider(object):

    '''快代理'''

    def __init__(self):
        self.exchange_id = ""
        self.page = 10
        self.result = []

    def get(self):
        for p in range(1, self.page+1):
            for item in self.get_one(p):
                self.result.append(item)
        return self.result

    def get_one(self, page):
        r = requests.get("https://www.kuaidaili.com/free/inha/{}/".format(page))

        retList = re.findall(r'<td data-title="IP">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>'
                         r'.*?<td data-title="PORT">(\d+)</td>.*?<td data-title="类型">(.*?)</td>', r.text, re.S)
        return retList

# print(ProxySpider().get_one(1))


# ips_list = ProxySpider().get()
#
# for item in ips_list:
#     proxyip, proxyport, proxytype = item
#     print("[?] Test {}://{}:{} ".format(proxytype, proxyip, proxyport))
#
#     stime = time.time()
#     if CheckProxy.check(proxyip, proxyport, proxytype):
#         etime = time.time()
#         print("[*] {}://{}:{} request speed {}s..".format(proxytype, proxyip, proxyport, int(etime-stime)))
