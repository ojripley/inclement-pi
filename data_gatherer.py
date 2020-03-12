#!/usr/bin/python
from sense_hat import SenseHat
import time
import sys

DATA_READ_INTERVAL = 60 # in seconds

sense = SenseHat()
sense.clear() # clears the LED matrix

try:
  while True:
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    
    temp = round(temp, 1)
    humidity = round(humidity, 1)
    pressure = round(pressure, 1)

    print("\n\n-- Weather Readout --")
    print("Temperature:  ", temp, "°C")
    print("Humidity:     ", humidity + "%")
    print("Pressure:     ", pressure, "mbar")

    time.sleep(DATA_READ_INTERVAL)

except KeyboardInterrupt:
  pass