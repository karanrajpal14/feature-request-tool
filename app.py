import json
import os
from flask import Flask, render_template, request, jsonify
from model import db, Feature, FeatureSchema, PRIORITY_MIN, PRIORITY_MAX
import datetime
from dotenv import load_dotenv
from marshmallow import ValidationError
from sqlalchemy.orm.exc import UnmappedInstanceError

# Setting App State
load_dotenv()
app = Flask(__name__)
conf = os.getenv("APP_SETTINGS")
app.config.from_object(conf)
db.init_app(app)

# Load schema for validation
feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)


# Index page
@app.route("/")
def index():
    return render_template("index.html")


""" API that allows you to fetch, add and delete feature requests """


@app.route("/api/v1/feature", methods=["GET", "POST"])
@app.route("/api/v1/feature/<id>", methods=["DELETE"])
def feature_api_endpoint(id=None):

    # Return all feature requests
    if request.method == "GET":
        all_features = Feature.query.order_by(Feature.client, Feature.priority).all()
        result = features_schema.dumps(all_features)
        return result

    # Add feature request
    if request.method == "POST":
        payload = request.get_json()

        # verify if all fields are present in the schema
        if not payload:
            return "Feature request is empty. Please fill in all the fields."

        try:
            data = feature_schema.load(payload)
        except ValidationError as err:
            return jsonify(err.messages), 422

        # fetch payload data if all fields present
        if not data.errors:
            title = payload["title"]
            description = payload["description"]
            client = payload["client"]
            priority = payload["priority"]
            product_area = payload["product_area"]
            deadline = datetime.datetime.strptime(
                payload["deadline"], "%Y-%m-%d"
            ).date()

            # add feature and commit to db
            new_feature = Feature(
                title, description, client, priority, product_area, deadline
            )
            db.session.add(new_feature)
            db.session.commit()

            return "Feature requested. Thank you!"
        else:
            # return missing fields error messages
            return jsonify(data.errors), 422


    if request.method == 'DELETE':
        feature = Feature.query.get(id)
    # Delete feature request
    if request.method == "DELETE":
        feature = Feature.query.get(id)
        try:
            db.session.delete(feature)
            db.session.commit()
        except UnmappedInstanceError:
            return "Feature ID does not exist", 422
        return "Deleted feature successfully"


""" Helper Methods """

# Route to create db
@app.route("/create_db", methods=["GET"])
def create_db():
    app_context = Flask(__name__)
    app_context.config.from_object(conf)
    db.init_app(app_context)
    db.create_all(app=app_context)
    addMockData()
    return "DB Created"


def addMockData():
    features = []
    features.append(
        Feature(
            title="Welcome",
            description="This is a Feature Request Tool. I built it using basic web technologies, Knockout JS and Flask.",
            client="Client A",
            priority=1,
            product_area="Billing",
            deadline=datetime.datetime.strptime("2018-03-17", "%Y-%m-%d").date(),
        )
    )
    features.append(
        Feature(
            title="Use the form to add requests",
            description="Add as many as you'd like.",
            client="Client A",
            priority=1,
            product_area="Billing",
            deadline=datetime.datetime.strptime("2018-03-17", "%Y-%m-%d").date(),
        )
    )
    features.append(
        Feature(
            title="Look at the footer",
            description="For more information about me and a link to the source code for this application. Play around with the application and I hope you like it.",
            client="Client A",
            priority=1,
            product_area="Billing",
            deadline=datetime.datetime.strptime("2018-03-17", "%Y-%m-%d").date(),
        )
    )

    for feature in features:
        db.session.add(feature)

    db.session.commit()


# Returns selectable priorities depending on selected client
@app.route("/filter_priorities/<client>", methods=["GET"])
def filter_priorities(client):
    # fetching only priorities column filtered by selected client
    fetch_current_priorities = (
        Feature.query.with_entities(Feature.priority).filter_by(client=client).all()
    )
    # creating a set of priorities to exclude from the fetched priorities
    exclude_priorities = set(list(sum(fetch_current_priorities, ())))
    # building a set of priorities to show in the dropdown
    include_priorities = list(
        set(range(PRIORITY_MIN, PRIORITY_MAX + 1)) - exclude_priorities
    )
    return jsonify(include_priorities)


if __name__ == "__main__":
    app.run()
