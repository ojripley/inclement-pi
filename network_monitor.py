import os
import re
import subprocess
import time

# run a subprocess and call speedtest-cli. Log its output to the shell and read it
speedtest_response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell = True, stdout=subprocess.PIPE).stdout.read().decode('utf-8'))

# parse response for the data we want
ping = re.findall('Ping:\s(.*?)\s', speedtest_response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', speedtest_response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', speedtest_response, re.MULTILINE)

ping=ping[0].replace(',', '.')
download=download[0].replace(',', '.')
upload=upload[0].replace(',', '.')

try:
  file = open('/home/pi/speedtest/speedtest.csv', 'a+')
  if (os.stat('/home/pi/speedtest/speedtest.csv')).st_size == 0:
    f.write('Date, Time, Ping (ms), Download (Mb/s), Upload (Mb/s)\r\n')
except:
  pass

file.write('{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, download, upload))

