from threading import Thread
import configparser
from flask import render_template, request, redirect
from Rollladensteuerung import app
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
    form = request.form
    form_dict = form.to_dict()

    # call client class to send data to shutter control server in a new thread
    # sends data "open" or "close" to specified ip on port 80

    def send_data():
        Client(form_dict['change'], (form_dict['ip'], 80))

    t1 = Thread(target=send_data)
    t1.start()
    return redirect('/')
