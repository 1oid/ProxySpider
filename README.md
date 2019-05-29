# ProxySpider
____
* 目录结构
```
➜  ProxySpider git:(master) ✗ tree
.
├── README.md
├── __init__.py
├── config.py
├── libs
│   ├── __init__.py
│   ├── checkproxy.py
│   ├── plugin.py
│   └── rabbitmq.py
├── main.py
├── plugins
│   ├── __init__.py
│   └── ip89.py
└── reciver.py

5 directories, 19 files
```

* 文件/目录说明
	+ `config.py` 配置文件, 配置rabbitmq服务器的地址/账号/密码
	+ `main.py` 主程序
	+ `reciver.py` 从队列获取任务(测试)
	+ `plugins` 代理爬虫插件
	+ `libs` 一些函数库

* 消费者的编写
```
实例 reciver.py
from ProxySpider.libs.rabbitmq import recive_task_one, recived_task
from ProxySpider.config import CHANNEL_ID
import json


# 回调
def callback(ch, method, properties, body):
    print("Recived body: {}".format(json.loads(body)))


recived_task(CHANNEL_ID, callback)
# print(recive_task_one(CHANNEL_ID))
```

* 运行截图(左为生产者, 将数据pulish到分布式队列, 右为编写的消费者, 一直从队列取出数据)
![image](https://user-images.githubusercontent.com/19285429/58568109-33de6a00-8266-11e9-9e49-273100074b01.png)