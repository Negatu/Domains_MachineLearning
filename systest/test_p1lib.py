
import os
import sys

db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "db" )
sys.path.append( db_dir )
import db_ops

p1_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Phase1" )
sys.path.append( p1_dir )
import p1lib

dbs_dir = os.path.join(db_dir, "dbs")
db_name = "scratch.db"
scratch_db = os.path.join(dbs_dir, db_name)

dom_table_size = 10000

ping_test = [ ["google",0], ["invalidpingurl",1], ["knnnknknknk",1], ["negatu", 0] ]

def test_populate_dom_table():
	dbops = db_ops.dbops(db_name)
	dbops.create_db()
	p1lib.populate_dom_table(dbops, dom_table_size)
	assert dbops.count_rows("DOMAINS") == dom_table_size
	print "Populate dom table test successful!"

def _setup():
	dbops = db_ops.dbops(db_name)
	dbops.create_db()
	for domain in ping_test:
		dbops.add_domain_name(domain[0])
	dbops.commit()
	return dbops

def test_populate_ping_table():
	dbops = _setup()
	p1lib.populate_ping_table(dbops, len(ping_test))
	for i in range (0, len(ping_test)):
		assert dbops.retrieve_ping_result(i+1) == ping_test[i][1]
	print "Populate ping table test successful!"


