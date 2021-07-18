from flask import render_template, request, redirect
from Rollladensteuerung import app, db
from Rollladensteuerung.models import Shutter
from Rollladensteuerung.client import ThreadClient


@app.route('/')
@app.route('/home')
def home():
    return render_template('dashboard.html')


@app.route('/<file>.html')
def test_content(file):
    if file in ['rollladen', 'rollladen-add', 'rollladen-edit', 'rollladen-delete']:
        return render_template(f'{file}.html', shutters=Shutter.query.all())
    else:
        return render_template(f'{file}.html')


@app.route('/handle_shutter_change', methods=['POST'])
def handle_shutter_change():
    # call client class to send data to shutter control server in a new thread
    # sends data "open" or "close" to specified ip on port 80
    ThreadClient(request.form['ip'], request.form['state']).start()

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
        Shutter.query.filter_by(room=request.form.get('room')).delete()
        db.session.commit()
        return redirect('/')


@app.route('/edit_shutter', methods=['GET', 'POST'])
def edit_shutter():
    if request.method == 'GET':
        return render_template('edit_shutter.html', shutters=Shutter.query.all())
    elif request.method == 'POST':
        Shutter.query.filter_by(id=request.form['id']).update(dict(room=request.form['room']))
        Shutter.query.filter_by(id=request.form['id']).update(dict(ip=request.form['ip']))
        db.session.commit()
        return redirect('/')
