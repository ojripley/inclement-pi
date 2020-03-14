import time
import sense
import asyncio

async def run_animation_async():
  await sense.sensing_animation(True)

try:
  run_animation_async()
  while True:

    climate_data = sense.read_data(True)


    time.sleep(1)

except KeyboardInterrupt:
    sense.clear()
    pass
