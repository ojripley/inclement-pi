import psutil
import time

from gpiozero import CPUTemperature

def get_system_data():
  system_data = dict()

  system_data['cpuPercent'] = psutil.cpu_percent()
  system_data['cpuTemperature'] = CPUTemperature()
  system_data['memoryPercent'] = psutil.virtual_memory()

  return system_data
