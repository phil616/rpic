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

