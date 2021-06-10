from flask import render_template, request, redirect
from Rollladensteuerung import app, db
from Rollladensteuerung.models import Shutter
from Rollladensteuerung.communication import Client


@app.route('/')
def home():
    return render_template('home.html', shutters=Shutter.query.all())


@app.route('/handle_shutter_change', methods=['POST'])
def handle_shutter_change():
    # call client class to send data to shutter control server in a new thread
    # sends data "open" or "close" to specified ip on port 80
    # Client(request.form['ip'], request.form['state'])

    update = Shutter.query.filter_by(room=request.form['room']).first()
    update.state = request.form['state']
    db.session.commit()

    return redirect('/')


@app.route('/add_shutter', methods=['GET', 'POST'])
def add_shutter():
    if request.method == 'GET':
        return render_template('add_shutter.html')
    elif request.method == 'POST':
        shutter = Shutter(room=request.form['room'], ip=request.form['ip'], state=request.form['state'])
        db.session.add(shutter)
        db.session.commit()
        return redirect('/')


@app.route('/delete_shutter', methods=['GET', 'POST'])
def delete_shutter():
    if request.method == 'GET':
        return render_template('delete_shutter.html', shutters=Shutter.query.all())
    elif request.method == 'POST':
        for room in request.form:
            Shutter.query.filter_by(room=room).delete()
            db.session.commit()
        return redirect('/')
