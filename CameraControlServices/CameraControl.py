#!/usr/bin/env python
import subprocess

from flask import Flask
import datetime
import flask
import redis
import os
from wrappers import GPhoto
from random import choice


app = Flask(__name__)
app.secret_key = 'asdf'
red = redis.StrictRedis()

camera = GPhoto(subprocess)

def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('camera-control')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']

@app.route('/')
def main():
    #return subprocess.check_output(["ls", "-l"])
    return flask.jsonify(success=True)

@app.route('/shot')
def shot():
    files = []
    for file in os.listdir("/CameraControl/raspberry-camera-control/CameraControlServices/pictures"):
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            files.append('/pictures/' + file)
    if files.count() > 0:
        filename = choice(files)
        return flask.jsonify(success=True, filename=filename)
    else:
        return flask.jsonify(success=False, message="Cannot take a picture")

@app.route('/images-list')
def imagesList():
    images = []
    for file in os.listdir("/CameraControl/raspberry-camera-control/CameraControlServices/pictures"):
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            images.append({'filename': '/pictures/' + file})
    return flask.jsonify(success=True, images=images)

@app.route('/stream')
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route('/update')
def update():
    #return subprocess.check_output(["ls", "-l"])

    try:
        cam = camera.get_camera_name()
    except:
        return flask.jsonify(success=False, message='No camera found')

    try:
        captured_file = camera.capture_image_and_download()
    except:
        return flask.jsonify(success=False, message='Could not take a picture')

    return flask.jsonify(success=True, camera=cam, filename=captured_file)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)