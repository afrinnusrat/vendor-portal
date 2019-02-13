from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app import db
import uuid
import datetime


class Histories(db.Model):
    __tablename__ = 'histories'
    id = db.Column(String(50), primary_key=True)
    created_time = db.Column(DateTime(), nullable=False)
    component_id = db.Column(String(50), ForeignKey('components.id'))

    def __init__(self, component_id):
        self.id = str(uuid.uuid4())
        self.created_time = datetime.datetime.now()
        self.component_id = component_id

    def __repr__(self):
        return '<History %r>' % (self.name)
