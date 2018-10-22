import sys

sys.path.insert(0, '.')
sys.path.insert(0, '..')

from Hydranet.db import DB, User, Customer, Graph, Data, Sensor, Alert
import ConfigParser
from os.path import expanduser

def openDatabase():
    config = ConfigParser.ConfigParser()
    config.read(expanduser('~/hydranetrc'))
    dbname = 'Database_test'
    c = {}
    c['host'] = config.get(dbname, 'host')
    c['user'] = config.get(dbname, 'user')
    c['password'] = config.get(dbname, 'password')
    c['database'] = config.get(dbname, 'database')

    db = DB()
    db.connect(c)
    return db

def test_User():
    db = openDatabase()
    assert db is not None

    u = User(db)
    assert u is not None

    # try to read non-existant record
    u.load('fred')
    assert u.row is None

    # load existing record
    u.load('jennifer@jsquared.co.uk')
    assert u.row['User_ID'] == 105
    assert u.row['Forename'] == 'Jennifer'
    assert u.row['Surname'] == 'Liddle'
    assert u.row['Email'] == 'jennifer@jsquared.co.uk'
    assert u.row['Administrator']
    assert u.row['IsCurrent']

    # validate password
    assert not u.validate('x')
    assert u.validate('xyzzy')

    cust = u.getCustomer()
    assert cust is not None
    assert cust.row['Abbreviation'] == 'J2'

def test_Data():
    db = openDatabase()
    assert db is not None

def test_Graph():
    db = openDatabase()
    assert db is not None

    g = Graph(db);
    assert g is not None

    graphs = g.listGraphs(101)
    assert len(graphs) == 2

def test_Alert():
    db = openDatabase()
    assert db is not None
    a = Alert(db)
    assert a is not None
    a.load(1)
    assert a.row['Sensor_ID'] == 500;
    assert a.row['User_ID'] == 105;
    assert a.row['Value'] == 15;
    rows = a.loadAll()
    assert len(rows) == 3
    assert rows[0]['Alert_ID'] == 1
    assert rows[1]['Sensor_ID'] == 500
    assert rows[2]['User_ID'] == 108

    
