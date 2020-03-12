import time
import asyncio
import websockets
# from sense_data_gatherer import Sensor
from network_monitor import NetworkMonitor

# climate_sensor = Sensor()
network_monitor = NetworkMonitor()

# in seconds
SENSE_READ_INTERVAL = 60  
NETWORK_READ_INTERVAL = 50 

async def forward_climate_data():
  while True:
    # climate_conditions = climate_sensor.read_data()
    # print(climate_conditions)
    print('getting climate data...')

    # todo: write a websocket protocol to send this to a frontend
    await asyncio.sleep(SENSE_READ_INTERVAL)

async def forward_network_data():
  while True:
    print('getting network data...')
    network_data = network_monitor.assess_network()
    print(network_data)
    await asyncio.sleep(NETWORK_READ_INTERVAL)


loop = asyncio.get_event_loop()
try:
  asyncio.ensure_future(forward_climate_data())
  asyncio.ensure_future(forward_network_data())
  loop.run_forever()

# break loop on ctrl+c
except KeyboardInterrupt:
  pass
