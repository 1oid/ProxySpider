import pika
import json
from config import RABBITMQ_PASS, RABBITMQ_SERVER, RABBITMQ_USER


def publish_task(channel_id, data):
    '''
    :param channel_id: 信道id, 区分队列
    :param data:
    :return:
    '''
    auth = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER, 5672, "/", auth))

    channel = connection.channel()

    channel.queue_declare(queue=channel_id, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=channel_id,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    print("[+] Pulished the {} into Rabbitmq.....".format(data))
    connection.close()


def recived_task(channel_id, callback):
    print("Reciving by CHANNEL_ID {}...".format(channel_id))
    auth = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER, 5672, "/", auth))

    channel = connection.channel()
    channel.queue_declare(queue=channel_id, durable=True)

    # def callback(ch, method, properties, body):
    #     print("[+] Recived: {}".format(body))

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=channel_id,
        auto_ack=True,
        on_message_callback=callback
    )
    channel.start_consuming()


def recive_task_one(channel_id):
    print("Reciving by CHANNEL_ID {}...".format(channel_id))
    auth = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER, 5672, "/", auth))

    channel = connection.channel()
    channel.queue_declare(queue=channel_id, durable=True)

    for i in channel.consume(channel_id):
        method_frame, propertites, body = i
        channel.basic_ack(method_frame.delivery_tag)
        connection.close()
        return json.loads(body)
