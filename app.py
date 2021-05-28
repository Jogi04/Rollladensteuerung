from flask import Flask, render_template, request, redirect
from communication import Client
from threading import Thread

app = Flask(__name__)

shutters = [
    {
        'room': 'Wohnzimmer',
        'ip': '192.168.178.89',
        'state': 'closed'
    },
    {
        'room': 'Schlafzimmer',
        'ip': '192.168.178.90',
        'state': 'open'
    },
    {
        'room': 'Esszimmer',
        'ip': '192.168.178.91',
        'state': 'open'
    }
]


@app.route('/')
def index():
    return render_template('home.html', shutters=shutters)


@app.route('/<room_name>')
def room(room_name):
    return render_template(f'{room_name.lower()}.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    form = request.form
    form_dict = form.to_dict()

    # call client class to send data to shutter control server in a new thread
    # sends data "open" or "close" to specified ip

    def send_data():
        Client(form_dict['change'], (form_dict['ip'], 80))

    t1 = Thread(target=send_data)
    t1.start()
    return redirect(f'/{form_dict["room"]}')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
