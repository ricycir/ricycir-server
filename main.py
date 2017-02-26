from flask import Flask, request
from os.path import join, dirname
import os
import io
from PIL import Image
from array import array
import socket
import sys
#from thread import *
import _thread
from clarifai.rest import ClarifaiApp, Image as ClImage
import pprint

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

cl = ClarifaiApp(os.environ.get('CLIENTID'), os.environ.get('CLIENT_SECRET'))

model = cl.models.get('general-v1.3')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 5001)
sock.bind(server_address)
sock.listen(1)

new_data = False

def recycle_type(tags):
  if isType(tags, 'plastic'):
    return 'p'
  if isType(tags, 'cardboard'):
    return 'c'
  if isType(tags, 'drink') or isType(tags, 'beer'):
    return 'm'

def client_thread(conn):
  global new_data
  while True:
    #data = conn[0].recv(1024)
    #print('d: ' + str(data, 'utf-8'))
    #if not data:
    #  break
    if new_data:
      r_type = recycle_type(img_tags)
      print('type -> ' + r_type)
      conn[0].sendall(bytes(r_type+'\r\n', encoding='utf-8'))
      new_data = False
  # out of loop so close connection
  conn[0].close()

app = Flask(__name__)

def isType(data, trash_type):
  for tag in data:
    if tag['name'] == trash_type:
      return True
  return False

@app.route("/rec_img", methods=['POST'])
def rec_img():
  file = request.files['uploaded']
  bytes = bytearray(file.read())
  image = Image.open(io.BytesIO(bytes))
  image.save("./test.bmp")
  climage = ClImage(file_obj=open('./test.bmp', 'rb'))
  pred = model.predict([climage])
  tags = pred['outputs'][0]['data']['concepts']
  input_data = pred['outputs'][0]['input']['data']
  pprint.PrettyPrinter(indent=4).pprint(tags)
  pprint.PrettyPrinter(indent=4).pprint(input_data)
  print("plastic: " + str(isType(tags, 'plastic')))
  print("cardboard: " + str(isType(tags, 'cardboard')))
  print("drink: " + str(isType(tags, 'drink')))
  print("beer: " + str(isType(tags, 'beer')))
  global new_data 
  new_data = True
  global img_tags 
  img_tags = tags
  return "recieved image"

def socket_server():
  while True:
    connection = sock.accept()
    global new_data
    print('New Socket conn')
    _thread.start_new_thread(client_thread, (connection,))

if __name__ == "__main__":
  _thread.start_new_thread(socket_server, ())
  app.run(host='0.0.0.0', port=5000)
