from threading import Thread
import configparser
from flask import render_template, request, redirect, copy_current_request_context
from Rollladensteuerung import app, db
from Rollladensteuerung.communication import Client


@app.route('/')
def home():
    config = configparser.ConfigParser()
    config.read('shutters.ini')
    shutters = []
    for i in config.sections():
        shutters.append(dict(config.items(i)))
    return render_template('home.html', shutters=shutters)


@app.route('/handle_shutter_change', methods=['POST'])
def handle_shutter_change():
    # call client class to send data to shutter control server in a new thread
    # sends data "open" or "close" to specified ip on port 80

    @copy_current_request_context
    def send_data():
        Client(request.form['ip'], request.form['change'])

    t1 = Thread(target=send_data)
    t1.start()

    shutter = (request.form['room'], request.form['change'], request.form['ip'])  # pass tuple to db
    db.session.add(shutter)
    db.session.commit()

    return redirect('/')
