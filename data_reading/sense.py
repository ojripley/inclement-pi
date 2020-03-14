import time
from gpiozero import CPUTemperature
from subprocess import PIPE, Popen
from sense_hat import SenseHat
import asyncio

sense = SenseHat()
class Sensor:
  e = [0, 0, 0]  # not lit
  r = [255, 0, 0]  # red
  o = [255, 127, 0]  # orange
  y = [255, 255, 0]  # yellow
  g = [0, 255, 0]  # green
  b = [0, 0, 255]  # blue
  i = [75, 0, 130]  # indigo
  v = [159, 0, 255]  # violet
  w = [255, 255, 255]  # white

  sample_frame = [
    r, o, y, g, b, i, v, w,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
  ]

  frame_1 = [
    b, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, b,
    o, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, o,
    b, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, b,
    o, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, o,
  ]

  frame_2 = [
    b, b, e, e, e, e, e, o,
    o, e, e, e, e, e, b, b,
    o, o, e, e, e, e, e, b,
    b, e, e, e, e, e, o, o,
    b, b, e, e, e, e, e, o,
    o, e, e, e, e, e, b, b,
    o, o, e, e, e, e, e, b,
    b, e, e, e, e, e, o, o,
  ]

  frame_3 = [
    b, b, b, e, e, e, o, o,
    o, o, e, e, e, b, b, b,
    o, o, o, e, e, e, b, b,
    b, b, e, e, e, o, o, o,
    b, b, b, e, e, e, o, o,
    o, o, e, e, e, b, b, b,
    o, o, o, e, e, e, b, b,
    b, b, e, e, e, o, o, o,
  ]

  frame_4 = [
    b, b, b, b, e, o, o, o,
    o, o, o, e, b, b, b, b,
    o, o, o, o, e, b, b, b,
    b, b, b, e, o, o, o, o,
    b, b, b, b, e, o, o, o,
    o, o, o, e, b, b, b, b,
    o, o, o, o, e, b, b, b,
    b, b, b, e, o, o, o, o,
  ]

  frame_4 = [
    b, b, b, b, v, o, o, o,
    o, o, o, v, b, b, b, b,
    o, o, o, o, v, b, b, b,
    b, b, b, v, o, o, o, o,
    b, b, b, b, v, o, o, o,
    o, o, o, v, b, b, b, b,
    o, o, o, o, v, b, b, b,
    b, b, b, v, o, o, o, o,
  ]

  current_frame = 0
  frames = [frame_1, frame_2, frame_3, frame_4]

  def get_cpu_temperature(self):
    """get cpu temperature using vcgencmd"""
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()

    return float(output[output.index('=') + 1:output.rindex("'")])

  # returns a dict of temperature, humidity and pressure
  def read_data(self, PRINT_OUT_PUT = False):
    # sense.clear() # clears the LED matrix
    self.sensing_animation(self.current_frame)
    if (self.current_frame == len(self.frames) - 1):
      self.current_frame = 0
    else:
      self.current_frame += 1

    print('current_frame:' + str(self.current_frame))
    print('total frames:' + str(len(self.frames)))

    climate_conditions = dict()

    # because cpu temp affects sense readings, we need to offest the raw data

    raw_temp = sense.get_temperature()
    cpu = CPUTemperature()

    # 5.446 was default value for this algorithim... not sure how accurate it is. will need to experiment
    adjusted_temp = raw_temp - ((cpu.temperature - raw_temp)/1.5)

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
  def sensing_animation(self, frame_index):


    sense.set_pixels(self.frames[frame_index])

  def test_display(self):
    sense.set_pixels(self.sample_frame)

  def clear(self):
    sense.clear()
