import time
import asyncio
import websockets
import json as json
# from sense_data_gatherer import Sensor
from network_monitor import NetworkMonitor

HOST = 'localhost'
PORT = 8080

# in seconds
SENSE_READ_INTERVAL = 1  
NETWORK_READ_INTERVAL = 10

# climate_sensor = Sensor()
network_monitor = NetworkMonitor()

# holds the most up-to-date data from each source
current_data = dict()

# holds all active client sockets
users = set()

async def get_current_data():
  return current_data

async def get_climate_data():
  while True:
    # climate_conditions = climate_sensor.read_data()
    # print(climate_conditions)
    print('getting climate data...')
    current_data['climate_data'] = 'climate data'

    await asyncio.sleep(SENSE_READ_INTERVAL)

async def get_network_data():
  while True:
    print('getting network data...')
    network_data = network_monitor.assess_network()

    current_data['network_data'] = network_data
    print(current_data)

    await asyncio.sleep(NETWORK_READ_INTERVAL)

async def register(socket):
  users.add(socket)

async def unregister(socket):
  users.remove(socket)

async def broadcast_data():
  print('broadcast is being run, sending to:')
  print(users)
  if users: # protect against empty set
    await asyncio.wait([user.send(json.dumps(current_data)) for user in users])

async def server(socket, path):
  await register(socket)
  
  try:
    print('preparing to broadcast')
    await broadcast_data()
  finally:
    await unregister(socket)

start_server = websockets.serve(server, HOST, PORT)

loop = asyncio.get_event_loop()
try:
  loop.run_until_complete(start_server)
  asyncio.ensure_future(get_climate_data())
  asyncio.ensure_future(get_network_data())
  loop.run_forever()

# break loop on ctrl+c
except KeyboardInterrupt:
  pass
