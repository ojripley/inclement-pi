#!/usr/bin/env python

import asyncio
import uvloop
import json
import time
import datetime
import websockets

# from sense import Sensor
from system import get_system_data
from dht22 import read_data

# sensor = Sensor()

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
hourly_averages['14'] = dict(temperature = [], humidity = [], pressure = [])
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
clients = set()

async def collect_data():
  while True:
    try:

      now = datetime.datetime.now()
      hr = now.hour
      temp_climate_data = read_data()
      print(temp_climate_data);
      climate_data = dict()
      
      if (temp_climate_data != None): # avoids setting climate data with checksum error
        climate_data = temp_climate_data

        if (hour_history['hour'] != hr):  # the hour has changed
          hour_history['hour'] = hr
          hour_history['temp'] = []
          hour_history['humidity'] = []

        # append current data, calculate current hour's average
        hour_history['temp'].append(climate_data['temperature'])
        hour_history['humidity'].append(climate_data['humidity'])

      temp_sum = 0
      humidity_sum = 0
      
      for temp in hour_history['temp']:
        temp_sum += temp
        
      if (len(hour_history['temp']) > 0):
        avg_temp = temp_sum / len(hour_history['temp'])
      else:
        avg_temp = None

      for humidity in hour_history['humidity']:
        humidity_sum += humidity

      if (len(hour_history['humidity']) > 0):
        avg_humidity = humidity_sum / len(hour_history['humidity'])
      else:
        avg_humidity = None

      # record average
      hr_key = str(hr)
      if (avg_temp != None and avg_humidity != None):
        hourly_averages[hr_key]['temperature'] = int(round(avg_temp))
        hourly_averages[hr_key]['humidity'] = int(round(avg_humidity))

      climate_data['hourly_averages'] = hourly_averages
      data['climateData'] = climate_data
      data['systemData'] = get_system_data()
      print('data read')

      await asyncio.sleep(3)
    except KeyboardInterrupt:
      pass


async def register(websocket):
  print('adding client')
  clients.add(websocket)
  print('clients: ' + str(len(clients)))


async def unregister(websocket):
  print('removing client')
  clients.remove(websocket)
  print('clients: ' + str(len(clients)))


async def socket_server(websocket, path):
  # register(websocket) sends user_event() to websocket
  await register(websocket)
  try:
    while True:
      await websocket.send(json.dumps(data))
      await asyncio.sleep(3)

      # async for message in websocket:
      #   msg = json.loads(message)
      #   print(msg)
      #   if (msg['request'] == 'network-test'):
      #       print('... net test ...')
      #       network_results = await assess_network()
      #       print(network_results)
        # elif data["action"] == "plus":
        #     STATE["value"] += 1
        #     await notify_state()

  finally:
      await unregister(websocket)

server_handle = websockets.serve(socket_server, '0.0.0.0', 8080)

asyncio.get_event_loop().run_until_complete(server_handle)
asyncio.get_event_loop().run_until_complete(collect_data())

asyncio.get_event_loop().run_forever()
