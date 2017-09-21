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

@app.before_request
def before_request():
    g.db = DB()
    g.db.connect(app.config)

#@app.teardown_request
#def teardown_request(exception):
    #db = getattr(g, 'db', None)
    #if db is not None:
        #db.close()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('graph'))
    return redirect(url_for('login'))

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
                customers=u.loadCustomers()
                session['Customer_ID']=customers['Customer_ID']
                return redirect(url_for('index'))
            else:
                msg = 'invalid password'
    return render_template('login.html', error=msg)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if 'username' not in session:
        return redirect(url_for('login'))
    graph = Graph(g.db)
    graphList = graph.listGraphs(session['Customer_ID'])
    return render_template('graph.html',graphs=graphList)

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

