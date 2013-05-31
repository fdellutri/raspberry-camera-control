import datetime
import flask
import redis


app = flask.Flask(__name__)
app.secret_key = 'asdf'
red = redis.StrictRedis()


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('chat')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']

@app.route('/stream')
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)
