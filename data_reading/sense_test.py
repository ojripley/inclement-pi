import time
from sense import Sensor
import asyncio

sensor = Sensor()

try:
  # sensor.sensing_animation(True)
  while True:

    climate_data = sensor.read_data(True)

    time.sleep(1)
except KeyboardInterrupt:
    sensor.clear()
    pass
