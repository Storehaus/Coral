from quart import websocket, current_app

async def _receive(token) -> None:
  while True:
    message = await websocket.receive()
    return_message = f"WS_CLIENT: {token}, MSG: {message}"
    await current_app.broker.publish(return_message)
    print(return_message)