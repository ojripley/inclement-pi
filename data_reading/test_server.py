import socket
import os
from threading import Thread
import threading
import time
import json
import datetime
import sense

# HOST = socket.gethostname()
HOST = '127.0.0.1'
PORT = 8080

clients = set()
clients_lock = threading.Lock()

s = socket.socket()
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT))
threads = []

def listener(client, address):
  print("Accepted connection from: ", address)
  with clients_lock:
    clients.add(client)
  try:
    while True:
      data_encoded = client.recv(1024)
      data = data_encoded.decode()
      if data == '0':
        # timestamp = datetime.datetime.now().strftime("%I:%M:%S %p")
        # client.send(timestamp.encode())

        climate_data = sense.read_data()
        data_string = json.dumps(climate_data)
        client.send(data_string.encode())
        time.sleep(2)
  finally:
    with clients_lock:
      clients.remove(client)
      client.close()

s.listen()
print('server is listening on ' + str(PORT))

while True:
  client, address = s.accept()
  threads.append(Thread(target=listener, args=(client, address)).start())
s.close()
