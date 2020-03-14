import time
import sense

try:
  sense.sensing_animation(True)
  while True:

    climate_data = sense.read_data(True)


    time.sleep(1)

except KeyboardInterrupt:
    sense.clear()
    pass
