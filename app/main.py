from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.templating import Jinja2Templates

from .redis_services import connection, redis_connector


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    async with connection.pubsub() as pubsub:
        await pubsub.psubscribe("channel:*")
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            message = message.get('data')
        else:
            message = ''
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": message,
    })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await redis_connector(websocket)

