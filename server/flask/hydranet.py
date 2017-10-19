#
# This is the main hydranet Flask application
#
# It is called from /var/www/hydranet/wsgi.py and typically lives in /usr/local/bin
#
#
from __future__ import print_function
import logging
import logging.handlers
import os
import time
import ConfigParser
from os.path import expanduser
import sys
import re
from flask import Flask, g, session, redirect, url_for, request, render_template, jsonify
from flask.json import JSONEncoder

sys.path.insert(0, '/usr/local/lib/python2.7')
from Hydranet.db import DB, User, Customer, Graph, Data

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            # Implement code to convert Passport object to a dict
            return obj.row
        else:
            JSONEncoder.default(self, obj)

# dev means we are running under a development environment rather than production
dev = os.environ.get('DEV','0') == '1'

if dev:
    app = Flask(__name__, template_folder='/var/www/hydranet_dev/templates', static_folder='/var/www/hydranet_dev/static')
else:
    app = Flask(__name__, template_folder='/var/www/hydranet/templates', static_folder='/var/www/hydranet/static')

#
# Set up logging
#
LOG_FILENAME = '/tmp/hydranet.log'
hlog = logging.getLogger(__name__)
hlog.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000, backupCount=3)
formatter = logging.Formatter('[%(asctime)s] - %(message)s')
handler.setFormatter(formatter)
hlog.addHandler(handler)
hlog.warn(time.asctime()+' Starting')
hlog.info(os.environ)

# Read configuration file
if dev:
    configFile = '/home/hydranet/hydranetrc.dev'
else:
    configFile = expanduser('~/hydranetrc')

config = ConfigParser.ConfigParser()
hlog.info(time.asctime()+" Reading configuration file: '" + configFile + "'")
config.read(configFile)

# set the secret key.  keep this really secret:
app.secret_key = 'This needs to be read from the config file'

dbname = 'Database_rw'
app.config['host'] = config.get(dbname, 'host')
app.config['user'] = config.get(dbname, 'user')
app.config['password'] = config.get(dbname, 'password')
app.config['database'] = config.get(dbname, 'database')

# Now tell Flask to use the custom class
app.json_encoder = CustomJSONEncoder

@app.errorhandler(500)
def internal_server_error(e):
    hlog.error('Server Error: %s', (e))
    return render_template('500.html',error=(e)), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    hlog.error('Unhandled Exception: %s', (e))
    return render_template('500.html',error=(e)), 500


#
# Before we action any request, we connect to the database
#
@app.before_request
def before_request():
    g.db = DB()
    g.db.connect(app.config)

#@app.teardown_request
#def teardown_request(exception):
    #db = getattr(g, 'db', None)
    #if db is not None:
        #db.close()

#
# The main page takes you to the graphs, or the login page
#
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('graph'))
    return redirect(url_for('login'))

#
# Logging in
#
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        u = User(g.db)
        msg = 'Invalid username or password'
        if u.load(request.form['username']) is None:
            msg = 'no such user'
        else:
            if u.validate(request.form['password']):
                session['username'] = u.row['Forename'] + ' ' + u.row['Surname']
                session['user'] = u
                customer=u.getCustomer()
                session['Customer_ID']=customer.row['Customer_ID']
            else:
                msg = 'invalid password'
    return render_template('login.html', error=msg)

#
# Logout
#
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

#
# Display all graphs for the current user
#
@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if 'username' not in session:
        return redirect(url_for('login'))
    graph = Graph(g.db)
    graphList = graph.listGraphs(session['Customer_ID'])
    return render_template('graph.html',graphs=graphList)

#
# Display a particular graph for a specified date range
#
@app.route('/data/<Graph_ID>/<days>')
def data(Graph_ID,days=1):
    graph = Graph(g.db)
    sensors = graph.listSensors(Graph_ID)
    data = []
    for sensor in sensors:
        dataset = graph.loadData(sensor['Sensor_ID'],days)
        data.append({'legend': sensor['Legend'], 'data': dataset})
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

