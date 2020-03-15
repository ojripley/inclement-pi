import psutil
import time


def get_cpu_temperature():
    """get cpu temperature using vcgencmd"""
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()

    return float(output[output.index('=') + 1:output.rindex("'")])

def get_system_data():
  print('cpu percent: ' + str())
  print('memory : ' + str(psutil.virtual_memory().percent))
  print('network :' + str(len(psutil.net_connections())))

  system_data = dict()

  system_data['cpuPercent'] = psutil.cpu_percent()
  system_data['cpuTemperature'] = get_cpu_temperature()
  system_data['memoryPercent'] = psutil.virtual_memory().percent()

  return system_data
