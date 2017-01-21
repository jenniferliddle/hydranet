import sys

sys.path.insert(0, '.')
sys.path.insert(0, '..')

from Hydranet.db import DB, User, Customer, Graph, Data
import ConfigParser
from os.path import expanduser

def test():
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


