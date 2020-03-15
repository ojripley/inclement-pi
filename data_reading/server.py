import time
import asyncio
import websockets
import json as json
from sense import Sensor
from network_monitor import NetworkMonitor

HOST = '0.0.0.0'
PORT = 8080

# in seconds
SENSE_READ_INTERVAL = 1  
NETWORK_READ_INTERVAL = 10

sensor = Sensor()
network_monitor = NetworkMonitor()

# holds the most up-to-date data from each source
current_data = dict()

# holds all active client sockets
users = set()

async def get_current_data():
  return current_data

async def get_climate_data():
  print('preparing to read data!')
  current_data['climate_data'] = sensor.read_data()
  time_of_reading = time.ctime(time.time())
  current_data['timestamp'] = time_of_reading
  print('just got data... im tired, going to sleep now') 
  time.sleep(1)
  print('quick nap is over!')


async def register(socket):
  print('registering' + str(socket))
  users.add(socket)

async def unregister(socket):
  users.remove(socket)

async def broadcast_data(socket):
  print('broadcast is being run, sending to:')
  print(socket)

  while True:
    # await socket.send(json.dumps(current_data))
    current_data = await get_current_data()
    if (users):
      await asyncio.wait([user.send(json.dumps(current_data)) for user in users])
      print('just sent data: ')
      print(current_data)



async def server(socket, path):
  await register(socket)

  try:
    print('preparing to broadcast')
    await broadcast_data(socket)
  finally:
    await unregister(socket)

start_server = websockets.serve(server, HOST, PORT)

loop = asyncio.get_event_loop()
try:
  loop.run_until_complete(start_server)
  asyncio.ensure_future(get_climate_data())
  print('server is listening at ' + str(HOST) + ':' +str(PORT))
  loop.run_forever()

# break loop on ctrl+c
except KeyboardInterrupt:
  sensor.clear()
  pass
