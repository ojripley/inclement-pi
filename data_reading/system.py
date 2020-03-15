import psutil
import time

from gpiozero import CPUTemperature


def get_cpu_temperature():
    """get cpu temperature using vcgencmd"""
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()

    return float(output[output.index('=') + 1:output.rindex("'")])

def get_system_data():
  system_data = dict()

  system_data['cpuPercent'] = psutil.cpu_percent()
  system_data['cpuTemperature'] = CPUTemperature()
  system_data['memoryPercent'] = psutil.virtual_memory().percent()

  return system_data
