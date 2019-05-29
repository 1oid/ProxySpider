import os
import sys


# 列所有插件的名字
def list_plugins(path):
    return [x[:-3] for x in list(filter(lambda x: (True, False)[x[:2] == '__' or x[-2:] != "py"], os.listdir(path)))]


# print(list_plugins("."))

# 加载路径到环境变量
def path_load(path_name):
    sys.path.append(os.getcwd() + path_name)


# 插件加载, 返回插件实例对象
def plugin_load(plugin_name):
    m = __import__(plugin_name)

    if hasattr(m, "ProxySpider"):
        plugin = getattr(m, "ProxySpider")()
        return plugin
    return None


# path_load("/../plugins")
# plugin_load("ip89")
