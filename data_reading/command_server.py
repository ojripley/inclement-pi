#!/usr/bin/env python

import asyncio
import uvloop
import json
import time

from sanic import Sanic
from sanic import response
from sanic.response import file
from sanic.websocket import ConnectionClosed
from picamera import PiCamera

camera = PiCamera()

app = Sanic(__name__)

app.ws_clients = set()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def handleRequest(request):
  print(request)
  if (request == 'image'):

    camera.start_preview()
    time.sleep(3) # allows camera to adjust light sensor
    camera.capture('/home/pi/inclement-pi/inclementImage.jpg')
    camera.stop_preview()

    image = open('/home/pi/inclement-pi/inclementImage.jpg', 'rb')

    imageBytes = image.read()

    print(imageBytes)

async def broadcast(message):
  broadcasts = [ws.send(message) for ws in app.ws_clients]
  for result in asyncio.as_completed(broadcasts):
    try:
      await result
    except ConnectionClosed:
      print("ConnectionClosed")
    except Exception as ex:
      template = "An exception of type {0} occurred. Arguments:\n{1!r}"
      message = template.format(type(ex).__name__, ex.args)
      print(message)
    except KeyboardInterrupt:
      pass


@app.websocket("/")
async def websocket(request, ws):
  app.ws_clients.add(ws)
  await ws.send(json.dumps("hello from server!"))
  print(f'{len(app.ws_clients)} clients')
  while True:

    dataString = await ws.recv()
    print('request: ' + dataString)
    
    data = json.loads(dataString)
    handleRequest(data['request'])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=9090, workers=1, debug=False)
