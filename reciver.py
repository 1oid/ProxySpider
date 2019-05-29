from libs.rabbitmq import recive_task_one, recived_task
from config import CHANNEL_ID
import json


def callback(ch, method, properties, body):
    print("Recived body: {}".format(json.loads(body)))


recived_task(CHANNEL_ID, callback)
# print(recive_task_one(CHANNEL_ID))


