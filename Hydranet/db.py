import MySQLdb as mdb
import hashlib
import json

class User:

    def __init__(self,db):
        self.con = db.con

    def load(self,email):
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from User where Email = %s', (email,))
        self.row = c.fetchone()
        return self.row

    def validate(self,password):
        return self.row['Password'] == hashlib.md5(password).hexdigest()

    def loadCustomers(self):
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from User_Customer where User_ID = %s', (self.row['User_ID'],))
        rows = c.fetchone() # FIXME there could be more than one row returned
        return rows

class Customer:

    def __init__(self,db):
        self.con = db.con

    def load(self,id):
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from Customer where Customer_ID = %s', (id,))
        self.row = c.fetchone()
        return self.row

class Data:

    def __init__(self,db):
        self.con = db.con

    def insert(self,unit,sensor,value):
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('insert into Data (Sensor_ID,Value) values (%s,%s)', (sensor,value))
        self.con.commit()

class Graph:
    def __init__(self,db):
        self.con = db.con

    def listGraphs(self, id):
        "List the graphs for a given Customer ID"
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from Graph where Customer_ID = %s and Visible=1 order by Graph_ID', (id,))
        graphs = c.fetchall()
        for graph in graphs:
            c.execute('select * from Graph_Sensor where Graph_ID = %s and Visible=1', (graph['Graph_ID'],))
            graph['Sensors'] = c.fetchall()
        return graphs

    def listSensors(self, id):
        "List the Sensors for a given Graph"
        c = self.con.cursor(mdb.cursors.DictCursor)
        c.execute('select * from Graph_Sensor where Graph_ID = %s and Visible=1', (id,))
        return c.fetchall()

    def loadData(self,id,interval):
        "Load data for a given sensor ID and interval (in days)"
        c = self.con.cursor()
        sql = '''select unix_timestamp(Reading_Date), value 
                                     from Data 
                                    where Sensor_ID = %s 
                                      and Reading_Date > (now() - interval %s day)
                                 order by Reading_Date'''
        c.execute(sql,(id,interval))
        return c.fetchall()



class DB:

    def connect(self, config):
        self.con = mdb.connect(config['host'], config['user'], config['password'], config['database']);
        return self.con

    def close(self):
        self.con.close()
    
