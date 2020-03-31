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

hour_history = dict()
hour_history['hour'] = datetime.datetime.now().hour
hour_history['temp'] = []
hour_history['humidity'] = []
hour_history['pressure'] = []
hourly_averages = dict()
hourly_averages['0'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['1'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['2'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['3'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['4'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['5'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['6'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['7'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['8'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['9'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['10'] = dict(temperature =[], humidity = [], pressure = [])
hourly_averages['11'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['12'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['13'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['15'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['16'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['17'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['18'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['19'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['20'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['21'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['22'] = dict(temperature = [], humidity = [], pressure = [])
hourly_averages['23'] = dict(temperature = [], humidity = [], pressure = [])

data = dict()
async def collect_data():
  while True:
    try:

      now = datetime.datetime.now()
      hr = now.hour
      climate_data = sensor.read_data()

      if (hour_history['hour'] != hr):  # the hour has changed
        hour_history['hour'] = hr
        hour_history['temp'] = []
        hour_history['humidity'] = []
        hour_history['pressure'] = []

      # append current data, calculate current hour's average
      hour_history['temp'].append(climate_data['temperature'])
      hour_history['humidity'].append(climate_data['humidity'])
      hour_history['pressure'].append(climate_data['pressure'])

      temp_sum = 0
      humidity_sum = 0
      pressure_sum = 0
      for temp in hour_history['temp']:
        temp_sum += temp
      avg_temp = temp_sum / len(hour_history['temp'])

      for humidity in hour_history['humidity']:
        humidity_sum += humidity
      avg_humidity = humidity_sum / len(hour_history['humidity'])

      for pressure in hour_history['pressure']:
        pressure_sum += pressure
      avg_pressure = pressure_sum / len(hour_history['pressure'])

      # record average
      hr_key = str(hr)
      hourly_averages[hr_key]['temperature'] = int(round(avg_temp))
      hourly_averages[hr_key]['humidity'] = int(round(avg_humidity))
      hourly_averages[hr_key]['pressure'] = int(round(avg_pressure))

      climate_data['hourly_averages'] = hourly_averages
      data['climateData'] = climate_data
      data['systemData'] = get_system_data()

      await asyncio.sleep(1)
    except KeyboardInterrupt:
      sensor.clear()
      pass

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

await collect_data()

@app.websocket("/")
async def websocket(request, ws):
  app.ws_clients.add(ws)
  await ws.send(json.dumps("hello from climate server!"))

  while True:
    await broadcast(json.dumps(data))

    await asyncio.sleep(10)
  

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, workers=1, debug=False)
