"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""
import aio_pika
from conf import config
from datetime import datetime, timedelta

async def connect_rabbitmq():
    connection = await aio_pika.connect_robust(config.MQ_URI)
    return connection

async def create_shared_queue(connection):
    channel = await connection.channel()
    queue = await channel.declare_queue(config.MQ_SHARE, exclusive=False)
    return queue

async def publish_message(connection, message:str):
    channel = await connection.channel()
    queue = await create_shared_queue(connection)
    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=queue.name
    )

async def handle_shared_message():
    connection = await connect_rabbitmq()
    queue = await create_shared_queue(connection=connection)
    
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = message.body.decode()
                ... # handle payload


async def publish_message_with_ttl(message:str):
    connection = await connect_rabbitmq()
    channel = await connection.channel()
    queue = await create_shared_queue(connection)
    
    expiration = datetime.now() + timedelta(seconds=5)
    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode(), expiration=expiration),
        routing_key=queue.name
    )

