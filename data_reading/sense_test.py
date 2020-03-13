import time
from sense_data_gatherer import Sensor

sensor = Sensor()

try:
	while True:

		sensor.read_data()

		time.sleep(1)
except KeyboardInterrupt:
		pass
