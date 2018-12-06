import json
import os
from flask import Flask, render_template, request, jsonify
from model import db, Feature, FeatureSchema, PRIORITY_MIN, PRIORITY_MAX
import datetime
from dotenv import load_dotenv
from marshmallow import ValidationError
from sqlalchemy.orm.exc import UnmappedInstanceError

load_dotenv()
app = Flask(__name__)
conf = os.getenv('APP_SETTINGS')
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
@app.route('/api/v1/feature/<id>', methods=['DELETE'])
def feature_api_endpoint(id=None):

    if request.method == 'GET':
        all_features = Feature.query.order_by(
            Feature.client, Feature.priority).all()
        result = features_schema.dumps(all_features)
        return result

    if request.method == 'POST':
        payload = request.get_json()

        if not payload:
            return 'Feature request is empty. Please fill in all the fields.'

        try:
            data = feature_schema.load(payload)
        except ValidationError as err:
            return jsonify(err.messages), 422

        if not data.errors:
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
        else:
            return jsonify(data.errors)


    if request.method == 'DELETE':
        feature = Feature.query.get(id)
        try:
            db.session.delete(feature)
            db.session.commit()
        except UnmappedInstanceError:
            return 'Feature ID does not exist', 422
        return 'Deleted feature successfully'

@app.route('/create_db', methods=['GET'])
def create_db():
    app_context = Flask(__name__)
    app_context.config.from_object(conf)
    db.init_app(app_context)
    db.create_all(app=app_context)
    return 'DB Created'

@app.route('/filter_priorities/<client>', methods=['GET'])
def filter_priorities(client):
    fetch_current_priorities = Feature.query.with_entities(Feature.priority).filter_by(client=client).all()
    exclude_priorities= set(list(sum(fetch_current_priorities, ())))
    include_priorities = list(set(range(PRIORITY_MIN, PRIORITY_MAX + 1)) - exclude_priorities)
    return jsonify(include_priorities)


if __name__ == '__main__':
    app.run()
