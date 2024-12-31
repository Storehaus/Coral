import asyncio
from quart import websocket, current_app

async def _receive(token) -> None:
  while True:
    try: 
      message = await websocket.receive()
      return_message = f"WS_CLIENT: {token}, MSG: {message}"
      await current_app.broker.publish(return_message)
      print(return_message)
    except asyncio.CancelledError:
      print(f"Recieve task for token {token} cancelled")
      break
    except Exception as e:
      print(f"Error in _receive for token {token}: {e}")
      break