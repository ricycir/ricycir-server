from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/rec_img")
def rec_img():
  file = request.files['img']
  file.save(os.path.join('./', filename))
  return "img"

if __name__ == "__main__":
  app.run()
