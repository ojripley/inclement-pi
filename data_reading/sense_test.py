import time
import sense

try:
  while True:

    climate_data = sense.read_data(True)

    sense.sensing_animation(True)

    time.sleep(1)

except KeyboardInterrupt:
    sense.clear()
    pass
