'''
Hydranet.DB

A set of classes to represent records from the Hydranet database
'''

import hashlib
import MySQLdb as mdb

class Customer(object):
    "Class to represent a Customer record"
    def __init__(self,db):
        self.con = db.con
        self.row = None

    def load(self,customer_id):
        "Load a customer record given a Customer_ID"
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from Customer where Customer_ID = %s', (customer_id,))
        self.row = c.fetchone()
        return self.row

class User(object):
    "Class to represent a user"
    def __init__(self,db):
        self.db = db
        self.con = db.con
        self.row = None

    def load(self,email):
        """Load a user record given an email address
        :Args:
            email (string): The email of the user record to load.

        :Returns:
            dict: a dict of fields of the loaded record

        :Example:
            u = User(db)
            fields = u.load('jennifer@jsquared.co.uk')
            print fields['Forename']

        """
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from User where Email = %s', (email,))
        self.row = c.fetchone()
        return self.row

    def validate(self,password):
        "Check that a given password is valid"
        return self.row['Password'] == hashlib.md5(password).hexdigest()

    def getCustomer(self):
        "Return the Customer record for this user"
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from User_Customer where User_ID = %s', (self.row['User_ID'],))
        rows = c.fetchone()
        customer = Customer(self.db)
        customer.load(rows['Customer_ID'])
        return customer

class Data(object):
    "Class to represent a data record"
    def __init__(self,db):
        self.con = db.con

    def insert(self,unit,sensor,value):
        "Add some data"
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('insert into Data (Sensor_ID,Value) values (%s,%s)', (sensor,value))
        self.con.commit()

class Graph(object):
    "Class to represent a Graph record"
    def __init__(self,db):
        self.con = db.con

    def listGraphs(self, customer_id):
        "List the graphs for a given Customer ID"
        c = self.con.cursor(mdb.cursors.DictCursor)
        sql = '''select * from Graph
                 where Customer_ID = %s and Visible=1
                 order by Graph_ID'''
        c.execute(sql, (customer_id,))
        graphs = c.fetchall()
        sql = 'select * from Graph_Sensor where Graph_ID = %s and Visible=1'
        for graph in graphs:
            c.execute(sql, (graph['Graph_ID'],))
            graph['Sensors'] = c.fetchall()
        return graphs

    def listSensors(self, graph_id):
        "List the Sensors for a given Graph"
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from Graph_Sensor where Graph_ID = %s and Visible=1', (graph_id,))
        return c.fetchall()

    def loadData(self,sensor_id,interval):
        "Load data for a given sensor ID and interval (in days)"
        c = self.con.cursor()
        sql = '''select unix_timestamp(Reading_Date), value
                                     from Data 
                                    where Sensor_ID = %s 
                                      and Reading_Date > (now() - interval %s day)
                                 order by Reading_Date'''
        c.execute(sql,(sensor_id,interval))
        return c.fetchall()

class DB(object):
    "Class to represent a database object"
    def __init__(self):
        self.con = None

    def connect(self, config):
        "Connect to the database"
        self.con = mdb.connect(config['host'],
                               config['user'],
                               config['password'],
                               config['database'])
        return self.con

    def close(self):
        "Close the database connection"
        self.con.close()

