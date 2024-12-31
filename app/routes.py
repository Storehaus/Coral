import asyncio
from quart import Blueprint, jsonify, request, websocket, current_app
from datetime import datetime, timedelta
from threading import Timer, Lock
from .handlers.receive import _receive as ReceiveWebSocket
from .handlers.send import _send as SendWebSocket



bp = Blueprint("routes", __name__)

cache_lock = Lock()

@bp.route("/ws/start", methods = ["GET"])
def initiate_ws():

  token = current_app.token_manager.create_new_token()

  # Build the Web Socket URL
  # TODO: update this to be conditionally set on the HOSTED instance FQDN/route
  host = request.host.split(":")[0]
  port = request.host.split(":")[1] if ":" in request.host else "80"
  ws_url = f"ws://{host}:{port}/ws/{token}"

  # Return the Web Socket URL
  return jsonify({"url": ws_url})


@bp.websocket("/ws/<token>")
async def ws_run(token) -> None:
  # Check if the token exists in the cache
  token_exists = current_app.token_manager.check_if_token_exists(token)

  if token_exists == False:
    return
  
  # Now we can remove it from the cache
  current_app.token_manager.remove_expired_token(token)

  print(f"WebSocket request for token: {token}")
  # try:
  #   task = asyncio.ensure_future(ReceiveWebSocket(token))
  #   async for message in current_app.broker.subscribe():
  #     await websocket.send(message)
  # finally:
  #   task.cancel()
  #   print("WS Closed")
  #   await task

  try:      
    # Use asyncio.gather to manage concurrent tasks
    await asyncio.gather(
      ReceiveWebSocket(token),
      SendWebSocket(token)
    )
  except asyncio.CancelledError:
    print(f"WebSocket connection for token {token} cancelled.")
  finally:
    print(f"WebSocket connection for token {token} closed.")