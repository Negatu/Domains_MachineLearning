
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

def test_populate_dom_table():
	dbops = db_ops.dbops(db_name)
	dbops.create_db()
	p1lib.populate_dom_table(dbops, dom_table_size)
	assert dbops.count_rows("DOMAINS") == dom_table_size
	print "Populate dom table test successful!"
