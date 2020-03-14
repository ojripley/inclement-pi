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

  # because cpu temp affects sense readings, we need to offest the raw data

  raw_temp = sense.get_temperature()
  cpu = CPUTemperature()

  # 5.446 was default value for this algorithim... not sure how accurate it is. will need to experiment
  adjusted_temp = raw_temp - ((cpu.temperature - raw_temp)/2)

  temperature = round(adjusted_temp, 0)
  humidity = round(sense.get_humidity(), 0)
  pressure = round(sense.get_pressure(), 1)

  time_of_reading = time.ctime(time.time())

  climate_conditions['temperature'] = temperature
  climate_conditions['humidity'] = humidity
  climate_conditions['pressure'] = pressure

  if (PRINT_OUT_PUT):
    print("\n\n-- Weather Readout --")
    print("Temperature:  " + str(temperature) + " C")
    print("Humidity:     " + str(humidity) + " %")
    print("Pressure:     " + str(pressure) + " mbar")
    print("Taken at:     " + str(time_of_reading))

  return(climate_conditions)

# dynamically changes the LED matrix in response to the weather conditions
def update_display_matrix(climate_conditions):

  e = [0, 0, 0] # not lit
  r = [255, 0, 0] # red
  o = [255, 127, 0] # orange
  y = [255, 255, 0] # yellow
  g = [0, 255, 0] # green
  b = [0, 0, 255] # blue
  i = [75, 0, 130] # indigo
  v = [159, 0, 255] # violet
  w = [255, 255, 255] # white

  sample = [
    r, o, y, g, b, i, v, w,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
  ]

  sense.set_pixels(sample)

def clear():
	sense.clear()
