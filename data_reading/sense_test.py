import time
import sense

try:
	while True:

		sense.read_data(True)

		time.sleep(1)
except KeyboardInterrupt:
		pass
