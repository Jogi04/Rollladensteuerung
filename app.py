from flask import Flask, render_template, request, redirect
from communication import Client
from threading import Thread


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/wohnzimmer')
def wohnzimmer():
    return render_template('wohnzimmer.html')


@app.route('/schlafzimmer')
def schlafzimmer():
    return render_template('schlafzimmer.html')


@app.route('/esszimmer')
def esszimmer():
    return render_template('esszimmer.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    form = request.form
    form_dict = form.to_dict()

    # call client class to send data to shutter control server in a new thread

    def send_data():
        Client(form_dict['change'], (form_dict['ip'], 80))

    t1 = Thread(target=send_data)
    t1.start()
    return redirect(f'/{form_dict["room"]}')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
