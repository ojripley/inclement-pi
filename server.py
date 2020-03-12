import time
import asyncio
# from sense_data_gatherer import Sensor
# from network_monitor

# climate_sensor = Sensor()

SENSE_READ_INTERVAL = 10  # in seconds
NETWORK_READ_INTERVAL = 5 # may shorten this, depends how resource intensive speedtest-cli is

async def forward_climate_data():
  while True:
    # climate_conditions = climate_sensor.read_data()
    # print(climate_conditions)
    print('getting climate data...')

    # todo: write a websocket protocol to send this to a frontend
    await asyncio.sleep(SENSE_READ_INTERVAL)

async def forward_network_data():
  while True:
    # network_data = 
    print('getting network data...')
    await asyncio.sleep(NETWORK_READ_INTERVAL)


loop = asyncio.get_event_loop()
try:
  asyncio.ensure_future(forward_climate_data())
  asyncio.ensure_future(forward_network_data())
  loop.run_forever()

# break loop on ctrl+c
except KeyboardInterrupt:
  pass
