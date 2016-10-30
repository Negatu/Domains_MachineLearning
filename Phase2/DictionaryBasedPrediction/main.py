
import os
import sys
import time

db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), "db" )
sys.path.append( db_dir )
import db_ops

db_name = "test_set1_1k.db"
dbops = db_ops.dbops(db_name)
test_set_size = dbops.count_rows("DOMAINS")

file = open("words.txt", "r")
words_list = file.readlines()

prediction = {}
for i in range(1, test_set_size + 1):
	dom_name = dbops.retrieve_domain_name(i)
	print "predicting " + str(i) + " - " + dom_name
	if (dom_name + "\n") in words_list:
		prediction[i] = 1
	else:
		prediction[i] = 0

ping_results = {}
for i in range(1, test_set_size +1):
	ping_result = dbops.retrieve_ping_result(i)
	ping_results[i] = ping_result

# Performance Analysis
correct_up = 0
correct_down = 0
incorr_up = 0
incorr_down = 0
for i in range(1, test_set_size + 1):
	if ( prediction[i]==1 and ping_results[i]==1 ):
		correct_up += 1
	elif ( prediction[i]==0 and ping_results[i]==0 ):
		correct_down += 1
	elif ( prediction[i]==1 and ping_results[i]==0 ):
		incorr_up += 1
	elif ( prediction[i]==0 and ping_results[i]==1 ):
		incorr_down += 1
	else:
		print "Error: unkown ping or prediction value"
		print "Prediction value  : " + str(prediction[i])
		print "Ping value : " + str(ping_results[i])
		sys.exit(1)

test_set_size_float = test_set_size + 0.0
print "\n Results - \n"
print "Correctly guessed : " + str((correct_up+correct_down)/test_set_size_float)
print "Incorrectly guessed : " + str((incorr_up+incorr_down)/test_set_size_float)
print "\n"
print "correctly guessed up : " + str(correct_up/test_set_size_float)
print "correctly guessed down : " + str(correct_down/test_set_size_float)
print "incorrectly guessed up : " + str(incorr_up/test_set_size_float)
print "incorrectly guessed down : " + str(incorr_down/test_set_size_float)

dbops.close_db()
