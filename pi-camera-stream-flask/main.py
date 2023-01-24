#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request, send_from_directory
from camera import VideoCamera
from time import sleep
from gpiozero import Motor
import os

speed = 0.5
turn_speed = 0.8

motor = Motor(9, 25)
motor2 = Motor(11, 8)

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture()
    return "None"

@app.route('/w/')
def w():
  motor.forward(speed)
  motor2.forward(speed)
  return render_template('index.html')

@app.route('/stop/')
def stop():
  motor.stop()
  motor2.stop()
  return render_template('index.html')

@app.route('/s/')
def s():
  motor.backward(speed)
  motor2.backward(speed)
  return render_template('index.html')

@app.route('/a/')
def a():
  motor.forward(turn_speed)
  motor2.backward(turn_speed)
  return render_template('index.html')
@app.route('/d/')
def d():
  motor.backward(turn_speed)
  motor2.forward(turn_speed)
  return render_template('index.html')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)

