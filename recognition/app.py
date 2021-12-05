from flask import Flask, jsonify
import json
import logging

app = Flask(__name__)

@app.route('/recognize', methods=['POST'])
def recognize():
    app.logger.info('recognizing default')
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [{'pubsubname': 'pubsub',
                      'topic': 'recognize',
                      'route': '/recognize'}]
    return jsonify(subscriptions)

@app.route('/')
def hello():
    return 'Recognition Default Service'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5002)    
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)  