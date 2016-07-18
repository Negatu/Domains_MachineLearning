
import random

'''
This script provides the functionalities needed for phase1 (generating domain names and ping results data)
'''

ll_ws = 3 # lower limit for size of domain name string
ul_ws = 10 # upper limit for size of domain name string

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def generate_dom_name():
	word_size = random.randrange(ll_ws, ul_ws+1)
	word = ""
	for i in range(0, word_size):
		word += random.choice(alphabet)
	return word

def populate_dom_table(db_cursor, psize):
	for i in range(0, psize):
		dom_name = generate_dom_name()
		db_cursor.add_domain_name(dom_name)
	db_cursor.commit()