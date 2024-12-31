from quart import current_app, websocket
import asyncio

async def _send(token: str) -> None:
  async for message in current_app.broker.subscribe():
    try:
      await websocket.send(message)
    except asyncio.CancelledError:
      print(f"Send task for token {token} cancelled.")
    except Exception as e:
      print(f"Error in _send for token {token}: {e}")