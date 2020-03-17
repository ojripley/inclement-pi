#!/usr/bin/env python

import asyncio
import uvloop
import json
import time
import websockets

from sanic import Sanic
from sanic import response
from sanic.response import file
from sanic.websocket import ConnectionClosed
from sense import Sensor
from system import get_system_data

sensor = Sensor()
app = Sanic(__name__)

app.ws_clients = set()
clients_to_remove = set()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def broadcast(message):
  for ws in app.ws_clients:
    try:
      await ws.send(message)
      print('attempting data send')
      print(ws)
    except websockets.ConnectionClosed:
      print('removing a client')
      clients_to_remove.add(ws)
    except Exception as ex:
      template = "An exception of type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(ex).__name__, ex.args)
      print(message)
    except KeyboardInterrupt:
      sensor.clear()
      pass
  # if (len(clients_to_remove) > 0):
    # await remove_dead_clients(clients_to_remove)

# async def remove_dead_clients(clients_to_remove):
#   for client in clients_to_remove:
#     app.ws_clients.remove(client)
  
#   clients_to_remove.clear()

@app.websocket("/")
async def websocket(request, ws):
  app.ws_clients.add(ws)
  await ws.send(json.dumps("hello from server!"))
  print(f'{len(app.ws_clients)} clients')
  while True:
    try:

      data = dict()
      time_of_reading = time.ctime(time.time())
      data['climateData'] = sensor.read_data()
      data['systemData'] = get_system_data()
      data['timestamp'] = time_of_reading
      await broadcast(json.dumps(data))
      time.sleep(5)
    except KeyboardInterrupt:
      sensor.clear()
      pass

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, workers=1, debug=False)
