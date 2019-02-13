from sqlalchemy import Column, Integer, String, DateTime
from app import db
from sqlalchemy.orm import relationship
import uuid
import datetime


class Components(db.Model):
    __tablename__ = 'components'
    id = db.Column(String(50), primary_key=True)
    name = db.Column(String(50))
    quantity = db.Column(Integer(), default=0)
    price = db.Column(Integer(), default=0)
    component_type = db.Column(String(50))
    vendor_sku = db.Column(String(50), unique=True)
    description = db.Column(String(100), nullable=True)
    created_time = db.Column(DateTime(), nullable=False)
    modified_time = db.Column(DateTime(), nullable=False)
    histories = db.relationship(
        'Histories',
        backref='components',
        cascade='all,delete'
    )

    def __init__(self, name, quantity, price, component_type, vendor_sku, description):
        self.id = str(uuid.uuid4())
        self.name = name
        self.quantity = quantity
        self.price = price
        self.component_type = component_type
        self.vendor_sku = vendor_sku
        self.description = description
        self.created_time = datetime.datetime.now()
        self.modified_time = datetime.datetime.now()

    def __repr__(self):
        return '<Vendor SKU %r>' % (self.vendor_sku)
