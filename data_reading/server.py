#!/usr/bin/env python

import asyncio
import uvloop
import json
import time

from sanic import Sanic
from sanic import response
from sanic.response import file
from sanic.websocket import ConnectionClosed
from sense import Sensor
from system import get_system_data

sensor = Sensor()
app = Sanic(__name__)

app.ws_clients = set()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def broadcast(message):
  broadcasts = [ws.send(message) for ws in app.ws_clients]
  for result in asyncio.as_completed(broadcasts):
    try:
      await result
    except ConnectionClosed:
      print(ConnectionClosed)
      print("ConnectionClosed")
    except Exception as ex:
      template = "An exception of type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(ex).__name__, ex.args)
      print(message)
    except KeyboardInterrupt:
      sensor.clear()
      pass

@app.websocket("/")
async def websocket(request, ws):
  app.ws_clients.add(ws)
  await ws.send(json.dumps("hello from server!"))
  print(f'{len(app.ws_clients)} clients')
  while True:

    data = dict()
    time_of_reading = time.ctime(time.time())
    data['climateData'] = sensor.read_data()
    data['systemData'] = get_system_data()
    data['timestamp'] = time_of_reading
    await broadcast(json.dumps(data))
    print('just sent data')
    time.sleep(0.5)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, workers=1, debug=False)
