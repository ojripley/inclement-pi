import socket
import os
from threading import Thread
import threading
import time
import datetime
import sense

# HOST = socket.gethostname()
HOST = 'localhost'
PORT = 8080

clients = set()
clients_lock = threading.Lock()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
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
        client.send(climate_data)
        time.sleep(2)
  finally:
    with clients_lock:
      clients.remove(client)
      client.close()

s.listen()

while True:
  client, address = s.accept()
  threads.append(Thread(target=listener, args=(client, address)).start())
s.close()
