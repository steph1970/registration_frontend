from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests
import time

REGISTRATION_SERVICE_HOST='localhost'
REGISTRATION_SERVICE_PORT='5001'

REGISTRATION_SERVICE_URL = 'http://%s:%s' % (REGISTRATION_SERVICE_HOST, REGISTRATION_SERVICE_PORT)
DASHBOARD_URL = '%s/dashboard' % REGISTRATION_SERVICE_URL
SUBMISSIONS_URL = '%s/submissions' % REGISTRATION_SERVICE_URL

app = Flask(__name__)
socketio = SocketIO(app, logger=True)

def load_submission():
    r = requests.get(DASHBOARD_URL)
    time.sleep(1)
    emit('logged_in', 'AA')
    return r

@app.route('/')
def hello_world():
    return render_template('index.html', name='Steph')  

@socketio.on('my event')
def loaded(data):
    load_submission()

@app.route('/submissions/<subm_id>', methods=['GET'])
def get_submission(subm_id=0):
    subm = requests.get(SUBMISSIONS_URL+'/'+subm_id)
    return render_template('submission_details.html', submission=subm.json())

@app.route('/submissions', methods=['GET'])
def get_submissions():
    response = requests.get(SUBMISSIONS_URL)
    json_subms = response.json()
    return render_template('submissions_list.html', submissions=json_subms.get("Submissions"))

@app.route('/submissions/<subm_id>/validate')
def submission_validate(subm_id):
    res = requests.post(SUBMISSIONS_URL+'/'+subm_id+'/validate')
    emit('invoice_created')

@socketio.on('generate_registration_invoice')
def generate_registration_invoice(subm_id):
    submission_validate(subm_id)

if __name__ == "__main__":
    socketio.run(app, debug=True)
