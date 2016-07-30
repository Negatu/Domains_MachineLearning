
import cookielib
import os
import platform
import random
import re
import sys
import threading
import time
import urllib2

db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "db" )
sys.path.append( db_dir )
import db_ops

'''
This script provides the functionalities needed for phase1 (generating domain names and ping results data)
'''

ll_ws = 3 # lower limit for size of domain name string
ul_ws = 5 # upper limit for size of domain name string

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

def _check_domain(domain):
	# check if a domain is registered 
	# got it from => http://www.techstiff.com/2013/12/check-domain-availability-with-python.html
	site='http://www.checkdomain.com/cgi-bin/checkdomain.pl?domain=' + domain
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        req = urllib2.Request(site, headers=hdr)
        response = urllib2.urlopen(req)
        data = response.read()
        pat = re.compile("has already been registered by the organization below")
        if pat.search(data) is None:
        	return 1
        else:
        	return 0

class DomainTablePointer():
	i = 1 # current index in dom table
	imax = -1 # maximum index in dom table, needs to be initialized to table size by caller first
	ilock = threading.Lock() # lock over the domain table index
	rlock = threading.Lock() # lock over domain name reading
	wlock = threading.Lock() # lock over ping writing

class pinger_thread(threading.Thread):
    def __init__(self, thread_id, db_name):
        threading.Thread.__init__(self)
        self.id = thread_id
        self.db_name = db_name
        self.count = 0

    def run(self):
    	my_cursor = db_ops.dbops(self.db_name)
    	do_process_domain = False
    	while (DomainTablePointer.i < DomainTablePointer.imax):
    		DomainTablePointer.ilock.acquire()
    		if (DomainTablePointer.i < DomainTablePointer.imax ):
    			domain_id = DomainTablePointer.i
    			DomainTablePointer.i += 1
	    		self.count += 1
	    		do_process_domain = True
	    	DomainTablePointer.ilock.release()
	    	if do_process_domain:
	    		print " thread - " +str(self.id)+ " - started domain : " +str(domain_id)

	    		DomainTablePointer.rlock.acquire()
	    		my_cursor.connect()
	    		dom_name = my_cursor.retrieve_domain_name(domain_id)
	    		my_cursor.disconnect()
	    		DomainTablePointer.rlock.release()

	    		ping_result = _check_domain(dom_name)

	    		DomainTablePointer.wlock.acquire()
	    		my_cursor.connect()
	    		my_cursor.add_ping_result(domain_id, ping_result)
	    		my_cursor.disconnect()
	    		DomainTablePointer.wlock.release()

	    		do_process_domain = False
	    		print " thread - " +str(self.id)+ " - completed domain : " +str(domain_id)

def populate_ping_table_mt(db_name, psize, startat=1, num_pinger_threads=1000):
	DomainTablePointer.i = startat
	DomainTablePointer.imax = psize+1
	db_cursor = db_ops.dbops(db_name)

	threads = []
	for thread_id in range(1, num_pinger_threads):
		threads += [pinger_thread(thread_id, db_name)]

	for t in threads:
		try:
			t.start()
		except:
			print str(t.id) + " fstart - " + str(sys.exc_info()[1])
			sys.exit(1)

	for t in threads:
		try:
			t.join()
		except:
			print str(t.id) + " didn't join - " + str(sys.exc_info()[1])
			sys.exit(1)

	db_cursor.commit()	

def populate_ping_table(db_cursor, psize, startat=1):
	domain_id = startat
	for i in range(0, psize):
		dom_name = db_cursor.retrieve_domain_name(domain_id)
		ping_result = _check_domain(dom_name)
		db_cursor.add_ping_result(domain_id, ping_result)
		domain_id += 1
	db_cursor.commit()