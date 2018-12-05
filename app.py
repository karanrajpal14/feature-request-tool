import json
import os
from flask import Flask, render_template, request, jsonify
from model import db, Feature, FeatureSchema
import datetime

app = Flask(__name__)
conf = os.environ['APP_SETTINGS']
app.config.from_object(conf)
db.init_app(app)

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)


def log(message):
    if conf == "config.DevelopmentConfig":
        print(message)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/feature', methods=['GET', 'POST'])
def feature_api_endpoint():

    if request.method == 'GET':
        all_features = Feature.query.order_by(
            Feature.client, Feature.priority).all()
        result = features_schema.dumps(all_features)
        return result

    if request.method == 'POST':
        payload = request.get_json()

        title = payload['title']
        description = payload['description']
        client = payload['client']
        priority = payload['priority']
        product_area = payload['product_area']
        deadline = datetime.datetime.strptime(
            payload['deadline'], '%Y-%m-%d').date()

        new_feature = Feature(title, description, client,
                              priority, product_area, deadline)

        db.session.add(new_feature)
        db.session.commit()

        return "Feature requested. Thank you!"


@app.route('/create_db')
def create_db():
    app_context = Flask(__name__)
    app_context.config.from_object(conf)
    db.init_app(app_context)
    db.create_all(app=app_context)
    return 'DB Created'


if __name__ == '__main__':
    app.run()
