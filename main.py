import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from ProxySpider.libs.rabbitmq import recived_task
from ProxySpider.libs.plugin import *
from ProxySpider.libs.checkproxy import CheckProxy
from ProxySpider.libs.rabbitmq import publish_task, recived_task
from ProxySpider.config import CHANNEL_ID
import logging

# logging.basicConfig(level=logging.INFO, format="%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s")

# 列出所有的插件
plugin_lists = list_plugins("./plugins")
# 添加环境变量
path_load("/plugins")

# 线程池
executer = ThreadPoolExecutor(max_workers=5)
executer_tasks = []
# executer.submit()

for plugin_name in plugin_lists:
    # 迭代加载插件
    plugin = plugin_load(plugin_name)
    print("[*] Loading {} plugin, description: {}".format(plugin_name, plugin.__doc__))

    # 查询结果 迭代检测
    proxy_list = list(set(plugin.get()))
    for r in proxy_list:
        proxyip, proxyport, proxytype = r
        print("[*] test {}://{}:{}".format(proxytype, proxyip, proxyport))

        # if CheckProxy.check(proxyip, proxyport, proxytype):
        #     logging.INFO("Success!!! {}://{}:{}..".format(proxytype, proxyip, proxyport))
        # 丢到线程池
        executer_tasks.append(executer.submit(CheckProxy.check, ((proxyip, proxyport, proxytype))))

    # 等待执行完毕
    for result in as_completed(executer_tasks):
        rs = result.result()

        if rs:
            publish_task(CHANNEL_ID, rs)



