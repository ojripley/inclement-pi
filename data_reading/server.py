#!/usr/bin/env python

import asyncio
import uvloop
import json
import time
import datetime
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

# climate_data = []
hour_history = dict()
hour_history['hour'] = datetime.datetime.now().hour
hour_history['temps'] = []
hourly_averages = dict()
hourly_averages['0'] = None
hourly_averages['1'] = None
hourly_averages['2'] = None
hourly_averages['3'] = None
hourly_averages['4'] = None
hourly_averages['5'] = None
hourly_averages['6'] = None
hourly_averages['7'] = None
hourly_averages['8'] = None
hourly_averages['9'] = None
hourly_averages['10'] = None
hourly_averages['11'] = None
hourly_averages['12'] = None
hourly_averages['13'] = None
hourly_averages['15'] = None
hourly_averages['16'] = None
hourly_averages['17'] = None
hourly_averages['18'] = None
hourly_averages['19'] = None
hourly_averages['20'] = None
hourly_averages['21'] = None
hourly_averages['22'] = None
hourly_averages['23'] = None

async def broadcast(message):
  for ws in app.ws_clients:
    try:
      await ws.send(message)
    except websockets.ConnectionClosed:
      clients_to_remove.add(ws)
    except Exception as ex:
      template = "An exception of type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(ex).__name__, ex.args)
    except KeyboardInterrupt:
      sensor.clear()
      pass
  if (len(clients_to_remove) > 0):
    await remove_dead_clients(clients_to_remove)

async def remove_dead_clients(clients_to_remove):
  for client in clients_to_remove:
    app.ws_clients.remove(client)
  
  clients_to_remove.clear()

@app.websocket("/")
async def websocket(request, ws):
  app.ws_clients.add(ws)
  await ws.send(json.dumps("hello from climate server!"))
  while True:
    try:

      data = dict()
      now = datetime.datetime.now()
      hr = now.hour
      climate_data = sensor.read_data()

      if (hour_history['hour'] != hr): # the hour has changed
        hour_history['hour'] = hr
        hour_history['temps'] = []



      # append current temp, calculate current hour's average
      hour_history['temps'].append(climate_data['temperature'])
      sum = 0
      for temp in hour_history['temps']:
        sum += temp
      avg = sum / len(hour_history['temps'])

      # record average
      hourly_averages[hr] = int(round(avg))

      climate_data['hourly_averages'] = hourly_averages
      data['climateData'] = climate_data
      data['systemData'] = get_system_data()

      await broadcast(json.dumps(data))
      await asyncio.sleep(1)
    except KeyboardInterrupt:
      sensor.clear()
      pass

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, workers=1, debug=False)
