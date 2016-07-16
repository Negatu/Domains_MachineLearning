
import os
import sqlite3
import sys

db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "db" )
sys.path.append( db_dir )
import db_ops

db_tables = [ "DOMAINS", "PINGS", "RESPONSES" ]

dbs_dir = os.path.join(db_dir, "dbs")
db_name = "scratch.db"
scratch_db = os.path.join(dbs_dir, db_name)


def test_create_db():
	if (os.path.isfile(scratch_db)):
		os.remove(scratch_db)
		if (os.path.isfile(scratch_db)):
			print "Error: Failed to delete scratch_db - " + scratch_db
			sys.exit(1)
	db_ops.create_db(db_name)
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