
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

class dbops():

	def __init__(self, db_name):
		self.db_name = db_name
		self.db_file = os.path.join(dbs_dir, self.db_name)
		self.conn = sqlite3.connect(self.db_file)
		self.cur = self.conn.cursor()

	def create_db(self):
		self.conn.close()
		os.remove(self.db_file)
		if (os.path.isfile(self.db_file)):
			print "Error: Failed to delete already existing database - " + self.db_name
		fs = open(schema_file,'r')
		sql = fs.read()
		self.conn = sqlite3.connect(self.db_file)
		self.cur = self.conn.cursor()
		self.cur.executescript(sql)

	def close_db(self):
		self.conn.close()

	def commit(self):
		self.conn.commit()

	def disconnect(self):
		self.conn.commit()
		self.conn.close()

	def connect(self):
		self.conn = sqlite3.connect(self.db_file)
		self.cur = self.conn.cursor()

	def count_rows(self, table_name):
		sql = "select count(*) from "+ table_name +";"
		self.cur.execute(sql)
		return (self.cur.fetchone()[0])

	def add_domain_name(self, dom_name):
		sql = "insert into DOMAINS (domain_name) values ('"+ dom_name +"');"
		self.cur.execute(sql)

	def add_ping_result(self, domain_id, response_id):
		sql = "insert into PINGS (_domain_id, _response_id) values ("+ str(domain_id) +", "+ str(response_id) +");"
		self.cur.execute(sql)

	def retrieve_domain_name(self, domain_id):
		sql = "select domain_name from DOMAINS where domain_id="+ str(domain_id) +";"
		self.cur.execute(sql)
		return (self.cur.fetchone()[0])

	def retrieve_ping_entry(self, ping_id):
		sql = "select * from PINGS where ping_id="+ str(ping_id) +";"
		self.cur.execute(sql)
		return (self.cur.fetchone())

	def retrieve_ping_result(self, domain_id):
		sql = "select * from PINGS where _domain_id="+ str(domain_id) +";"
		self.cur.execute(sql)
		return (self.cur.fetchone()[2])
