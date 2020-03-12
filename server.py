import time
import asyncio
# from sense_data_gatherer import Sensor
# from network_monitor

# climate_sensor = Sensor()

SENSE_READ_INTERVAL = 6  # in seconds
NETWORK_READ_INTERVAL = 10 # may shorten this, depends how resource intensive speedtest-cli is

async def forward_climate_data(loop):

  # climate_conditions = climate_sensor.read_data()
  # print(climate_conditions)
  print('getting climate data...')

  # todo: write a websocket protocol to send this to a frontend
  await asyncio.sleep(SENSE_READ_INTERVAL)

async def forward_network_data():
  # network_data = 
  print('getting network data...')
  await asyncio.sleep(NETWORK_READ_INTERVAL)

loop = asyncio.get_event_loop()
loop.run_unti(forward_climate_data(loop))
# loop.run_forever(forward_network_data)