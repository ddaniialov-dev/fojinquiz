import socketio


sio = socketio.AsyncServer(
    cors_allowed_origins='*', async_mode='asgi'
)


@sio.on('chat_message', namespace='/chat')
async def chat_message(sid, data):
    await sio.emit('chat_message', data=data, namespace='/chat')
