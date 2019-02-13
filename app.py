from flask import Flask, render_template, request, redirect
from sqlalchemy import desc
from database import db_session, init_db
from flask_sqlalchemy import SQLAlchemy
from models.components import Components
from models.histories import Histories
from flask_migrate import Migrate
import datetime
import os

@app.before_first_request
def init():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def start():
    now = datetime.datetime.now()
    return render_template('start.html', nav='start', now=now)

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
        db_session.add(component)
        db_session.commit()

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

        db_session.commit()

        history = Histories(component_id=component.id)

        db_session.add(history)
        db_session.commit()

        return redirect('/components')

    return render_template('edit_component.html', component=component)


@app.route('/delete-component')
def delete_component():
    id = request.args.get('id')

    component = Components.query.filter(Components.id == id).first()

    if component:
        db_session.delete(component)
        db_session.commit()

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
