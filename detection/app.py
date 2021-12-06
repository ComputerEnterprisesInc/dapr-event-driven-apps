from flask import Flask, jsonify
import requests
import json
import os
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
daprPort = os.environ.get('DAPR_HTTP_PORT',  3500)

## Detection Endpoint
@app.route('/detect', methods=['POST'])
def detect():
    app.logger.info('Detecting default')
    publish_recognize_event({ 'result': 'default' })    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [{'pubsubname': 'pubsub',
                      'topic': 'detect',
                      'route': '/detect'}]
    return jsonify(subscriptions)

## Publish event to the event bus
def publish_recognize_event(event):
    app.logger.info(f'Publishing into recognize topic: {event}')
    requests.post(
        f'http://localhost:{daprPort}/v1.0/publish/pubsub/recognize', json=event)    

@app.route('/')
def hello():
    return 'Detection Service'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001) 
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)  