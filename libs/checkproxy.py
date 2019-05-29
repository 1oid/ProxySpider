import requests
import re
from config import CHECK_TIMEOUT
import urllib3
import socket
import time


class CheckProxy(object):

    def __init__(self):
        pass

    @staticmethod
    def check(item):
        s = time.time()

        proxyip, proxyport, proxytype = item
        proxytype = proxytype.lower()
        proxies = {
            proxytype: "{}://{}:{}".format(proxytype, proxyip, proxyport)
        }
        try:
            r = requests.get("http://2019.ip138.com/ic.asp", timeout=CHECK_TIMEOUT, proxies=proxies)
        except requests.exceptions.ReadTimeout as e:
            return False
        except requests.exceptions.ChunkedEncodingError as e:
            return False
        except requests.exceptions.ConnectTimeout as e:
            return False
        except requests.exceptions.ProxyError as e:
            return False
        except urllib3.exceptions.ReadTimeoutError as e:
            return False
        except socket.timeout as e:
            return False
        except requests.exceptions.ConnectionError as e:
            return False

        try:
            m = re.search(r'您的IP是：\[(.*?)\]', r.content.decode("gbk"))
        except UnicodeDecodeError as e:
            return False

        if m:
            e = time.time()
            if m.group(1).strip() == proxyip:
                return {"proxyip": proxyip, "proxyport": proxyport, "proxytype": proxytype, "ms": int(e-s)}
        return False


def CheckThreadExecuter():
    # CheckProxy.
    pass
# CheckProxy.check("", "", "")
