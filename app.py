from flask import Flask, render_template, request, redirect
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route('/')
def start():
    return render_template('start.html', nav='start')

@app.route('/create-component', methods=['GET', 'POST'])
def create_component():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        vendor_sku = request.form.get('vendor_sku')
        description = request.form.get('description')
        component_type = request.form.get('component_type')

        component = Components(name=name, quantity=quantity, price=price, vendor_sku=vendor_sku, description=description, component_type=component_type)
        db.session.add(component)
        db.session.commit()

        return redirect('/components')

    return render_template('create_component.html')


@app.route('/components')
def component_list():
    components = Components.query.all()

    return render_template('component.html', nav='component', components=components)


@app.route('/edit-component', methods=['GET', 'POST'])
def edit_component():
    id = request.args.get('id')

    component = Components.query.filter(Components.id == id).first()

    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        vendor_sku = request.form.get('vendor_sku')
        description = request.form.get('description')
        component_type = request.form.get('component_type')

        component.name = name
        component.quantity = quantity
        component.price = price
        component.vendor_sku = vendor_sku
        component.description = description
        component.component_type = component_type
        component.modified_time = datetime.datetime.now()

        db.session.add(component)
        db.session.commit()

        history = Histories(component_id=component.id)

        db.session.add(history)
        db.session.commit()

        return redirect('/components')

    return render_template('edit_component.html', component=component)


@app.route('/delete-component')
def delete_component():
    id = request.args.get('id')

    component = Components.query.filter(Components.id == id).first()

    if component:
        db.session.delete(component)
        db.session.commit()

    return redirect('/components')


@app.route('/history')
def history():
    histories = Histories.query.order_by(desc(Histories.created_time)).limit(20)

    return render_template('history.html', nav='history', histories=histories)


@app.route('/top')
def top():
    components = Components.query.order_by('-quantity').limit(5)

    return render_template('top.html', nav='top', components=components)


def datetimeformat(value):
    return value.strftime('%Y-%m-%d %H:%M:%S')


app.jinja_env.filters['datetime'] = datetimeformat

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)