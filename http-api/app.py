from flask import Flask
import json
import requests
import os
import logging

# from dapr import DaprClient
# daprClient = DaprClient()

daprPort = os.environ.get('DAPR_HTTP_PORT',  3500)

app = Flask(__name__)

@app.route('/trigger')
def trigger():
    app.logger.info('Triggering detection')
    publish_detect_event({'data': 'some data'})
    return json.dumps({'status': 'success'})

def publish_detect_event(event):
    # daprClient.publish_event('detection', 'detect', event)
    app.logger.info(f'Publishing into detect topic: {event}')
    requests.post(f'http://localhost:{daprPort}/v1.0/publish/pubsub/detect', json=event)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)