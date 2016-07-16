
import os
import sqlite3
import time

'''
This script provides an interface to interact with the databases in /db/dbs
'''

db_dir = os.path.dirname(os.path.realpath(__file__))
dbs_dir = os.path.join(db_dir, "dbs")
schema_filename = "db_schema.sql"
schema_file = os.path.join(db_dir, schema_filename)

def create_db(db_name=""):
	if (db_name == ""):
		db_name = time.time()
	conn = sqlite3.connect(os.path.join(dbs_dir, db_name))
	cur = conn.cursor()
	fs = open(schema_file,'r')
	sql = fs.read()
	cur.executescript(sql)
