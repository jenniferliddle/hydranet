from __future__ import print_function
from flask import Flask, g, session, redirect, url_for, escape, request, render_template, jsonify
from flask.json import JSONEncoder, dumps
from flaskext.mysql import MySQL
from Hydranet.db import DB, User, Customer, Graph, Data
import ConfigParser
from os.path import expanduser
import sys
import re

app = Flask(__name__, template_folder='/var/www/hydranet/templates', static_folder='/var/www/hydranet/static')

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            # Implement code to convert Passport object to a dict
            return obj.row
        else:
            JSONEncoder.default(self, obj)

import logging
logging.basicConfig(stream=sys.stderr)

config = ConfigParser.ConfigParser()
config.read(expanduser('~/hydranetrc'))

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

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

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
        if (u.load(request.form['username']) == None):
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
    if not 'username' in session:
        return redirect(url_for('login'))
    graph = Graph(g.db)
    graphList = graph.listGraphs(session['Customer_ID'])
    return render_template('graph.html',graphs=graphList)

@app.route('/data/<Graph_ID>')
def data(Graph_ID):
    graph = Graph(g.db)
    sensors = graph.listSensors(Graph_ID)
    data = []
    for s in sensors:
        d = graph.loadData(s['Sensor_ID'],1)
        data.append({'legend': s['Legend'], 'data': d})
    return jsonify({'data': data})

@app.route('/upload', methods=['GET', 'POST'])
def update():
    #print(request.form['data'], file=sys.stderr)
    m=re.search('T(.+)V.*\[(.+)\]',request.form['data'])
    value = m.group(1)
    unit = m.group(2)
    #print ("Unit: "+str(unit)+"  Temp: "+str(value), file=sys.stderr)
    d = Data(g.db)
    unit=800;
    d.insert(unit,unit,value)
    # Flask is unhappy if we don't return *something*
    return 'Done!';

from werkzeug.debug import DebuggedApplication
app.wsgi_app = DebuggedApplication( app.wsgi_app, True )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8088, debug=True)

