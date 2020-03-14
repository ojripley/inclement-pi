import time
import sense

try:
  while True:

    climate_data = sense.read_data(True)

    sense.update_display_matrix(climate_data)

    time.sleep(1)

except KeyboardInterrupt:
    sense.clear()
    pass
