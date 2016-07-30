
import test_db_ops as tdb
import test_p1lib as tp1

# Tests

tdb.test_create_db()
tdb.test_db_funcs()
tp1.test_populate_dom_table()
tp1.test_populate_ping_table()
tp1.test_populate_ping_table_multi_thread()

print "ALL TESTS SUCCESSFUL! "
