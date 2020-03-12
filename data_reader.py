import time
import asyncio
# from sense_data_gatherer import Sensor
from network_monitor import NetworkMonitor


# in seconds
SENSE_READ_INTERVAL = 60  
NETWORK_READ_INTERVAL = 50

# climate_sensor = Sensor()
network_monitor = NetworkMonitor()

# will hold the most up-to-date data from each source
current_data = dict()

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

loop = asyncio.get_event_loop()
try:
  asyncio.ensure_future(get_climate_data())
  asyncio.ensure_future(get_network_data())
  loop.run_forever()

# break loop on ctrl+c
except KeyboardInterrupt:
  pass
