import time
import asyncio
import websockets
import json as json
import sense
from network_monitor import NetworkMonitor

HOST = '0.0.0.0'
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

async def broadcast_data(socket):
  print('broadcast is being run, sending to:')
  print(socket)
  while True:
    climate_data = sense.read_data()
    current_data['climateData'] = climate_data
    
    socket.send(json.dumps(current_data))
    # await asyncio.wait()

    time.sleep(2)

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
  print('server is listening at ' + str(HOST) + ':' +str(PORT))
  loop.run_forever()

# break loop on ctrl+c
except KeyboardInterrupt:
  pass
