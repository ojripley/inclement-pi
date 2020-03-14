import time
import sense
import asyncio

async def sense_continuously():
  try:
    await sense.sensing_animation(True)
    while True:

      climate_data = sense.read_data(True)

      time.sleep(1)
  except KeyboardInterrupt:
      sense.clear()
      pass

sense_continuously()
