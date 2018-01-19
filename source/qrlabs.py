import logging
import logging.handlers
import os
from flask import Flask, request, redirect, url_for, render_template, Response, send_from_directory
import sqlite3
from datetime import datetime
from gevent.wsgi import WSGIServer
from functools import wraps
import time

import pdfexport
import database


def create_logger():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.handlers.RotatingFileHandler("qrLabs.log.log")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'admin'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)
UPLOAD_FOLDER = '/root/qrLabs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
database_handler = None
LOGGER = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        courses = database_handler.get_all_courses()
        return render_template('index.html', courses=courses)
    except Exception as e:
        LOGGER.error("Error in index(): "+str(e))


@app.route('/formulaire', methods=['GET'])
@requires_auth
def formulaire():
    try:
        location = request.args.get('location')
        return render_template('formulaire.html', location=location)
    except Exception as e:
        LOGGER.error("Error in formulaire(): "+str(e))


@app.route('/confirm', methods=['POST'])
@requires_auth
def confirm():
    try:
        location = request.form['location']
        quantity = request.form['quantity']
        return render_template('confirm.html', location=location, quantity=quantity)
    except Exception as e:
        LOGGER.error("Error in confirm(): "+str(e))


@app.route('/save', methods=['POST'])
@requires_auth
def save():
    try:
        location = request.form['location']
        quantity = request.form['quantity']
        database_handler.insert_course(location, quantity)
        result = "OK"
        return render_template('save.html', result=result)
    except Exception as e:
        LOGGER.error("Error in save(): "+str(e))


@app.route('/export', methods=['POST'])
@requires_auth
def export():
    try:
        data = database_handler.get_all_courses()
        pdfexport.export_courses(data)
        uploads = os.path.join(app.config['UPLOAD_FOLDER'])
        return send_from_directory(directory=uploads, filename='export.pdf')
    except Exception as e:
        LOGGER.error("Error in export(): "+str(e))


if __name__ == '__main__':
    create_logger()
    database_handler = database.DatabaseHandler()
    app.run(host='', port=80, debug=True)
    #http_server = WSGIServer(('', 80), app)
    #http_server.serve_forever()
