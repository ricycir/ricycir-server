from flask import Flask, request
import os
import io
from PIL import Image
from array import array
import socket
import sys
#from thread import *
import _thread
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 5001)
sock.bind(server_address)
sock.listen(1)

new_data = False
print('print test')
def client_thread(conn):
  while True:
    data = conn.recv(1024)
    if not data:
      break
    if new_data:
      print('socket msg')
      conn.sendall('Test')
      new_data = False
  # out of loop so close connection
  conn.close()

app = Flask(__name__)

@app.route("/rec_img", methods=['POST'])
def rec_img():
  file = request.files['uploaded']
  bytes = bytearray(file.read())
  image = Image.open(io.BytesIO(bytes))
  image.save("./test.bmp")
  return "recieved image"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
  
  while True:
    connection = sock.accept()
    new_data = True
    _thread.start_new_thread(client_thread, (connection,))
