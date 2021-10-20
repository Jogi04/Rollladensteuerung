import json
from flask import render_template, request, redirect
from Rollladensteuerung import app
from Rollladensteuerung.client import ThreadClient


@app.route('/')
@app.route('/home')
def home():
    return render_template('dashboard.html')


@app.route('/<file>.html')
def test_content(file):
    if file in ['rollladen', 'rollladen-add', 'rollladen-edit', 'rollladen-delete']:
        with open('Rollladensteuerung/shutters.json', 'r') as json_file:
            shutters_data = json.load(json_file)
            json_file.close()
        return render_template(f'{file}.html', shutters=shutters_data['rooms'])
    else:
        return render_template(f'{file}.html')


@app.route('/handle_shutter_change', methods=['POST'])
def handle_shutter_change():
    # call client class to send data to shutter control server in a new thread
    # sends data "open" or "close" to specified ip on port 80
    ThreadClient(request.form['ip'], request.form['state']).start()

    with open('Rollladensteuerung/shutters.json', 'r') as json_file:
        shutters_data = json.load(json_file)
        json_file.close()

    for i in shutters_data['rooms']:
        if i['room'] == request.form['room']:
            i['state'] = request.form['state']

    with open('Rollladensteuerung/shutters.json', 'w') as out_file:
        out_file.write(json.dumps(shutters_data, indent=4))
        out_file.close()

    return redirect('/')


@app.route('/add_shutter', methods=['POST'])
def add_shutter():
    if request.method == 'GET':
        return render_template('add_shutter.html')
    elif request.method == 'POST':
        with open('Rollladensteuerung/shutters.json', 'r') as json_file:
            shutters_data = json.load(json_file)
            json_file.close()

        shutters_data['rooms'].append({
            'room': request.form['room'],
            'ip': request.form['ip'],
            'state': request.form['state']
        })

        with open('Rollladensteuerung/shutters.json', 'w') as out_file:
            out_file.write(json.dumps(shutters_data, indent=4))
            out_file.close()

        return redirect('/')


@app.route('/edit_shutter', methods=['POST'])
def edit_shutter():
    with open('Rollladensteuerung/shutters.json', 'r') as json_file:
        shutters_data = json.load(json_file)
        json_file.close()

    for i in shutters_data['rooms']:
        if i['room'] == request.form['room']:
            i['ip'] = request.form['ip']

    with open('Rollladensteuerung/shutters.json', 'w') as out_file:
        out_file.write(json.dumps(shutters_data, indent=4))
        out_file.close()

    return redirect('/')


@app.route('/delete_shutter', methods=['POST'])
def delete_shutter():
    with open('Rollladensteuerung/shutters.json', 'r') as json_file:
        shutters_data = json.load(json_file)
        json_file.close()

    for i in shutters_data['rooms']:
        if i['room'] == request.form['room']:
            shutters_data['rooms'].remove(i)

    with open('Rollladensteuerung/shutters.json', 'w') as out_file:
        out_file.write(json.dumps(shutters_data, indent=4))
        out_file.close()

    return redirect('/')


@app.route('/settings_change', methods=['POST'])
def settings_change():
    with open('Rollladensteuerung/settings.json', 'w') as out_file:
        out_file.write(json.dumps(request.form.to_dict(), indent=4))
        out_file.close()

    return redirect('/')
