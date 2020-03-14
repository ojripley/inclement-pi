import socket
import os
import time
import json

s = socket.socket()
# HOST = socket.gethostname()
HOST = '192.168.1.155'
PORT = 8080

s.connect((HOST, PORT))
while True:
    s.send('0'.encode())
    data_encoded = s.recv(1024)
    data = data_encoded.decode()
    print(data)
