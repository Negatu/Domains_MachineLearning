
import os
import sys
import time

db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "db" )
sys.path.append( db_dir )
import db_ops

p1_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Phase1" )
sys.path.append( p1_dir )
import p1lib as p1

db_name = "experiment_zero.db"
dom_table_size = 200

dbops = db_ops.dbops(db_name)
dbops.create_db()

p1.populate_dom_table(dbops, dom_table_size)
stime = time.time()
p1.populate_ping_table_mt(db_name, psize=dom_table_size, num_pinger_threads=200)
print " Ping Table Populated! TOOK : " + str(time.time()-stime) + "  seconds"

dbops.commit()
dbops.close_db()