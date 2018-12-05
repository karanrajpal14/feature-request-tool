import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)
conf = os.environ['APP_SETTINGS']
app.config.from_object(conf)

def log(message):
    if conf == "config.DevelopmentConfig":
        print(message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request_feature', methods=['POST'])
def save_feature_request():
    feature_request = request.get_json()
    log(feature_request)
    return json.dumps(feature_request)

if __name__ == '__main__':
    app.run()