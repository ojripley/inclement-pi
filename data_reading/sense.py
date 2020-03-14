import time
from gpiozero import CPUTemperature
from subprocess import PIPE, Popen
from sense_hat import SenseHat

sense = SenseHat()

def get_cpu_temperature():
  """get cpu temperature using vcgencmd"""
  process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
  output, _error = process.communicate()
  return float(output[output.index('=') + 1:output.rindex("'")])



# returns a dict of temperature, humidity and pressure
def read_data(PRINT_OUT_PUT = False):
  sense.clear() # clears the LED matrix

  climate_conditions = dict()

  raw_temp = sense.get_temperature()

  cpu = CPUTemperature()

  # 5.446 was default value for this algorith... not sure how accurate it is. will need to experiment
  # adjusted_temp = raw_temp - ((cpu.temperature - raw_temp)/5.446)
  adjusted_temp = raw_temp - ((cpu.temperature - raw_temp)/2.5)

  temperature = round(adjusted_temp, 1)
  humidity = round(sense.get_humidity(), 1)
  pressure = round(sense.get_pressure(), 1)

  time_of_reading = time.ctime(time.time())

  climate_conditions['temperature'] = temperature
  climate_conditions['humididty'] = humidity
  climate_conditions['pressure'] = pressure


  if (PRINT_OUT_PUT):
    print("\n\n-- Weather Readout --")
    print("Temperature:  " + str(temperature) + " C")
    print("Humidity:     " + str(humidity) + " %")
    print("Pressure:     " + str(pressure) + " mbar")
    print("Taken at:     " + str(time_of_reading))

  return(climate_conditions)

# dynamically changes the LED matrix in response to the weather conditions
def update_display_matrix(self, climate_conditions):
  print('todo!')
