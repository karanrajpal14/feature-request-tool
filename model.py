from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
from flask_marshmallow import Marshmallow
import os
import uuid

from marshmallow import fields, Schema, validates, ValidationError

db = SQLAlchemy()

PRIORITY_MIN = 1
PRIORITY_MAX = 10

class Feature(db.Model):
    __tablename__ = 'feature'

    id = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    client = db.Column(db.String, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    product_area = db.Column(db.String, nullable=False)
    deadline = db.Column(db.Date, nullable=False)

    def __init__(self, title, description, client, priority, product_area, deadline):
        self.title = title
        self.description = description
        self.client = client
        self.priority = priority
        self.product_area = product_area
        self.deadline = deadline


class FeatureSchema(Schema):
    id = fields.UUID()
    title = fields.String(required=True)
    description = fields.String(required=True)
    client = fields.String(required=True)
    priority = fields.Integer(required=True)
    product_area = fields.String(required=True)
    deadline = fields.Date(required=True)

    @validates('priority')
    def validate_priority(self, priority):
        if priority < PRIORITY_MIN or priority > PRIORITY_MAX:
            raise ValidationError('Priority must be between 1 and 10')

