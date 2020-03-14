import time
import asyncio
import websockets
import json as json
import sense
from network_monitor import NetworkMonitor

HOST = 'localhost'
PORT = 8080

# in seconds
SENSE_READ_INTERVAL = 1  
NETWORK_READ_INTERVAL = 10

network_monitor = NetworkMonitor()

# holds the most up-to-date data from each source
current_data = dict()

# holds all active client sockets
users = set()

async def get_current_data():
  return current_data

async def register(socket):
  print('registering' + str(socket))
  users.add(socket)

async def unregister(socket):
  users.remove(socket)

async def broadcast_data():
  print('broadcast is being run, sending to:')
  print(users)

  climate_data = sense.read_data()

  if users: # protect against empty set
    await asyncio.wait([user.send(json.dumps(climate_data)) for user in users])

  time.sleep(2)

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
  loop.run_forever()

# break loop on ctrl+c
except KeyboardInterrupt:
  pass
