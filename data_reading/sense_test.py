import time
import sense

try:
	while True:

		climate_conditions = sense.read_data(True)
    sense.update_display_matrix(climate_conditions)
		time.sleep(1)
except KeyboardInterrupt:
		pass
