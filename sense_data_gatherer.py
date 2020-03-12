#!/usr/bin/python
from sense_hat import SenseHat


class Sensor:
  def __init__(self):
    self.sense_hat = SenseHat()
    self.temperature = 0
    self.humidity = 0
    self.pressure = 0


  # returns a dict of temperature, humidity and pressure
  def read_data(self):
    self.sense_hat.clear() # clears the LED matrix

    climate_conditions = dict()

    self.temperature = round(self.sense_hat.get_temperature(), 1)
    self.humidity = round(self.sense_hat.get_humidity(), 1)
    self.pressure = round(self.sense_hat.get_pressure(), 1)

    climate_conditions['temperature'] = self.temperature
    climate_conditions['humididty'] = self.humidity
    climate_conditions['pressure'] = self.pressure

    print("\n\n-- Weather Readout --")
    print("Temperature:  ", self.temperature, "°C")
    print("Humidity:     ", self.humidity + "%")
    print("Pressure:     ", self.pressure, "mbar")

    print(climate_conditions)

    return(climate_conditions)

  # dynamically changes the LED matrix in response to the weather conditions
  def update_display_matrix(self, climate_conditions):
    print('todo!')