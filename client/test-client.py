# import asyncio
# import websockets


# async def hello():
#   uri = "ws://localhost:8080"
#   async with websockets.connect(uri) as websocket:

#     print('awaiting messages')

#     msg = await websocket.recv()
#     print(f"< {msg}")

# asyncio.get_event_loop().run_until_complete(hello())
# asyncio.get_event_loop().run_forever()


import socket
import os
import time
import json

s = socket.socket()
HOST = socket.gethostname()
PORT = 8080

s.connect((HOST, PORT))
while True:
    s.send('0'.encode())
    data_encoded = s.recv(1024)
    data = data_encoded.decode()
    print(data)
#s.close()
