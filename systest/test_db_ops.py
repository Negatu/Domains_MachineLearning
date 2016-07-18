
import os
import sqlite3
import sys
import unittest

db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "db" )
sys.path.append( db_dir )
import db_ops

db_tables = [ "DOMAINS", "PINGS", "RESPONSES" ]

domains = [ "google", "negatu", "formidable"]
pings = [ [4, 3], [2, 1], [5, 7] ]

dbs_dir = os.path.join(db_dir, "dbs")
db_name = "scratch.db"
scratch_db = os.path.join(dbs_dir, db_name)

def test_create_db():
	if (os.path.isfile(scratch_db)):
		os.remove(scratch_db)
		if (os.path.isfile(scratch_db)):
			print "Error: Failed to delete scratch_db - " + scratch_db
			sys.exit(1)
	dbops = db_ops.dbops(db_name)
	dbops.create_db()
	if not (os.path.isfile(scratch_db)):
		print "Error: Failed to create db file - " + scratch_db
		sys.exit(1)
	conn = sqlite3.connect(scratch_db)
	cur = conn.cursor()
	for table_name in db_tables:
		sql = " SELECT * from "+table_name + "; "
		try:
			cur.execute(sql)
		except:
			print("Error while testing table - " + table_name, sys.exc_info()[0])
			sys.exit(1)

	print "database creation test successful!"


def _setup():
	dbops = db_ops.dbops(db_name)
	dbops.create_db()
	for domain_name in domains:
		dbops.add_domain_name(domain_name)
	for ping_result in pings:
		dbops.add_ping_result(ping_result[0], ping_result[1])
	dbops.commit()
	return dbops

def test_db_funcs():
	dbops = _setup()
	assert dbops.count_rows("DOMAINS") == len(domains)
	assert dbops.count_rows("PINGS") == len(pings)
	for i in range(0, len(domains)):
		assert dbops.retrieve_domain_name(i+1) == domains[i]
	for i in range(0, len(pings)):
		assert dbops.retrieve_ping_entry(i+1) == tuple([i+1] + pings[i])
	for i in range(0, len(pings)):
		assert dbops.retrieve_ping_result(pings[i][0]) == pings[i][1] 

	print "database functions test successful!"