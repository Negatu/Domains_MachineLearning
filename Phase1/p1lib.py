
import platform
import os
import random

'''
This script provides the functionalities needed for phase1 (generating domain names and ping results data)
'''

ll_ws = 3 # lower limit for size of domain name string
ul_ws = 10 # upper limit for size of domain name string

alphabet = 'abcdefghijklmnopqrstuvwxyz'
extension = '.com'

def _generate_dom_name():
	word_size = random.randrange(ll_ws, ul_ws+1)
	word = ""
	for i in range(0, word_size):
		word += random.choice(alphabet)
	return word

def populate_dom_table(db_cursor, psize):
	for i in range(0, psize):
		dom_name = _generate_dom_name()
		db_cursor.add_domain_name(dom_name)
	db_cursor.commit()

def _ping_domain(address):
	if platform.system() == "Windows":
		response = os.system("ping "+ address +" -n 1")
	else:
		response = os.system("ping -c 1 " + address)
	if response == 0:
		return response
	else:
		return 1

def populate_ping_table(db_cursor, psize, startat=1):
	domain_id = startat
	for i in range(0, psize):
		dom_name = db_cursor.retrieve_domain_name(domain_id) 
		address = dom_name + extension
		ping_result = _ping_domain(address)
		db_cursor.add_ping_result(domain_id, ping_result)
		domain_id += 1
	db_cursor.commit()