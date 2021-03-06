#!/usr/bin/env python

import asyncio
import uvloop
import json
import time

from sanic import Sanic
from sanic import response
from sanic.response import file
from sanic.websocket import ConnectionClosed
import websockets
from picamera import PiCamera
from network_monitor import assess_network

camera = PiCamera()
camera.rotation = 180

app = Sanic(__name__)

app.ws_clients = set()
clients_to_remove = set()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def take_image():
    camera.start_preview()
    time.sleep(2)  # allows camera to adjust light sensor
    camera.capture('/home/pi/inclement-pi/inclementImage.jpg')
    camera.stop_preview()

    image = open('/home/pi/inclement-pi/inclementImage.jpg', 'rb')

    return image.read()

async def handle_request(request):
  payload = None
  if (request == 'image'):
    print('IMAGE REQUESTED')
    payload = take_image()
  elif (request == 'network-test'):
    print('network-test requested')
    network_results = await assess_network()

    temp = dict()

    temp['type'] = 'network-results'
    temp['data'] = network_results

    payload = json.dumps(temp)

  await broadcast(payload)

async def broadcast(message):

  # data = dict()
  # data['type'] = 'image'
  # data['data'] = message.decode()

  print('sending')
  # print(data)

  for ws in app.ws_clients:
    try:
      await ws.send(message)
    except websockets.ConnectionClosed:
      clients_to_remove.add(ws)
    except Exception as ex:
      template = "An exception of type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(ex).__name__, ex.args)
    except KeyboardInterrupt:
      pass
  await remove_dead_clients(clients_to_remove)

async def remove_dead_clients(clients_to_remove):
  for client in clients_to_remove:
    app.ws_clients.remove(client)

  clients_to_remove.clear()

@app.websocket("/")
async def websocket(request, ws):
  app.ws_clients.add(ws)
  while True:

    dataString = await ws.recv()
    
    data = json.loads(dataString)
    await handle_request(data['request'])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=9090, workers=1, debug=False)
