import time
from gpiozero import CPUTemperature
from subprocess import PIPE, Popen
from sense_hat import SenseHat

def get_cpu_temperature():
  """get cpu temperature using vcgencmd"""
  process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
  output, _error = process.communicate()
  return float(output[output.index('=') + 1:output.rindex("'")])


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

    raw_temp = self.sense_hat.get_temperature()

    cpu = CPUTemperature()

    # 5.446 was default value for this algorith... not sure how accurate it is. will need to experiment
    # adjusted_temp = raw_temp - ((cpu.temperature - raw_temp)/5.446)
    adjusted_temp = raw_temp - ((cpu.temperature - raw_temp)/3)

    self.temperature = round(adjusted_temp, 1)
    self.humidity = round(self.sense_hat.get_humidity(), 1)
    self.pressure = round(self.sense_hat.get_pressure(), 1)

    time_of_reading = time.ctime(time.time())

    climate_conditions['temperature'] = self.temperature
    climate_conditions['humididty'] = self.humidity
    climate_conditions['pressure'] = self.pressure


    print("\n\n-- Weather Readout --")
    print("Temperature:  " + str(self.temperature) + " C")
    print("Humidity:     " + str(self.humidity) + " %")
    print("Pressure:     " + str(self.pressure) + " mbar")
    print("Taken at:     " + str(time_of_reading))

    return(climate_conditions)

  # dynamically changes the LED matrix in response to the weather conditions
  def update_display_matrix(self, climate_conditions):
    print('todo!')
