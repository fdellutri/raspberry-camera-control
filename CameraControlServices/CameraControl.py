#!/usr/bin/env python
import subprocess

import time
from flask import Flask
import datetime
import flask
import redis
import os
from wrappers import GPhoto
from wrappers import Wrapper
from random import choice
import random, string
import os.path
import piggyphoto

app = Flask(__name__)
app.secret_key = 'asdf'
red = redis.StrictRedis()

#camera = GPhoto(subprocess)
wrapper = Wrapper(subprocess)

def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('camera-control')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

@app.route('/')
def main():
    #return subprocess.check_output(["ls", "-l"])
    return flask.jsonify(success=True)

@app.route('/shot')
def shot():
    picture_folder = "/CameraControl/raspberry-camera-control/CameraControlServices/pictures"
    filename = 'cc_' + randomword(10) + '.jpg'

    try:
        C = piggyphoto.Camera()
        C.capture_image("%s/%s" % (picture_folder, filename))
        return flask.jsonify(success=True, filename='/pictures/' + filename)
    except Exception as e:
        print e
        return flask.jsonify(success=False, message="Cannot take a picture")
    # try:
    #     #camera.capture_image_and_download()
    #     files = []
    #     for file in os.listdir("/CameraControl/raspberry-camera-control/CameraControlServices/pictures"):
    #         if file.endswith(".jpg") or file.endswith(".jpeg"):
    #             files.append('/pictures/' + file)
    #     if len(files) > 0:
    #         filename = choice(files)
    #         return flask.jsonify(success=True, filename=filename)
    #     else:
    #         return flask.jsonify(success=False, message="Cannot take a picture")
    # except Exception as e:
    #     print e
    #     return flask.jsonify(success=False, message="Cannot take a picture")

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

@app.route('/poweroff')
def poweroff():
    code, out, err = wrapper.call("sudo sudo shutdown -h now")
    if code != 0:
        print err
        return flask.jsonify(success=False, message="Failed to poweroff")
    return flask.jsonify(success=True, message=out)

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
