import asyncio
import logging

from fastapi.websockets import WebSocket, WebSocketDisconnect
import redis.asyncio as redis


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
connection = redis.Redis(
    host='redis',
    port=6379,
    decode_responses=True,
)


async def redis_connector(websocket: WebSocket):
    """
    Функция для подключения к Redis в режиме Pub/Sub(издатель-подписчик).
    Схема взаимодействия:

    1) Веб-браузер подключается к серверу по веб-сокету;
    2) Когда происходит событие, back-end отправляет данные в клиент по веб-сокету
    3) Клиент получает данные и отображает событие в режиме реального времени
    """

    async def consumer_handler(connection: redis, ws: WebSocket):
        """ Получение данных из вебсокета. """
        try:
            while True:
                message = await ws.receive_text()
                if message:
                    await connection.publish("channel:1", message)
        except WebSocketDisconnect as exc:
            logger.error(exc)

    async def producer_handler(
        pubsub: redis.client.PubSub,
        ws: WebSocket,
    ):
        """ Отправление данных в вебсокет. """
        try:
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True
                )
                if message:
                    await ws.send_text(message.get("data"))
        except Exception as exc:
            logger.error(exc)

    async with connection.pubsub() as pubsub:
        """ Подключаемся к активным каналам Redis. """
        await pubsub.psubscribe("channel:*")

        consumer_task = asyncio.create_task(consumer_handler(
            connection=connection,
            ws=websocket
        ))
        producer_task = asyncio.create_task(producer_handler(
            pubsub=pubsub,
            ws=websocket
        ))

        """
        При помощи модуля Asyncio создаем асинхронные задачи,
        для записи данных в Redis и получения данных из него.
        """
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        logger.info("\tDone task: {done}!")
        for task in pending:
            logger.debug(f"\tCanceled task: {task}.")
            task.cancel()

