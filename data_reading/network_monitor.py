import os
import re
import subprocess
import time

async def assess_network():

  print('reading network...')

  network_stats = dict()

  # run a subprocess and call speedtest-cli. Log its output to the shell and read it
  speedtest_response = subprocess.Popen('/home/pi/.local/bin/speedtest-cli --simple', shell = True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

  # parse response for the desired data
  ping = re.findall(r'Ping:\s(.*?)\s', speedtest_response, re.MULTILINE)
  download = re.findall(r'Download:\s(.*?)\s', speedtest_response, re.MULTILINE)
  upload = re.findall(r'Upload:\s(.*?)\s', speedtest_response, re.MULTILINE)

  network_stats['ping'] = ping[0].replace(',', '.')
  network_stats['download'] = download[0].replace(',', '.')
  network_stats['upload'] = upload[0].replace(',', '.')

  print(network_stats)

  return(network_stats)

  # def log_results(self):
  #   try:
  #     file = open('/home/pi/speedtest/speedtest.csv', 'a+')
  #     if (os.stat('/home/pi/speedtest/speedtest.csv')).st_size == 0:
  #       file.write('Date, Time, Ping (ms), Download (Mb/s), Upload (Mb/s)\r\n')
  #   except:
  #     pass

  #   file.write('{}, {}, {}, {}, {}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, download, upload))

