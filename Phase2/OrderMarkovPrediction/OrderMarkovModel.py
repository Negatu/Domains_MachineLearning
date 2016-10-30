
import time

class Model:
	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	def __init__(self):
		self.model = {}
		self.initModel()

	def initModel(self):
		for l in Model.alphabet:
			self.model[l] = {}
			for i in Model.alphabet:
				self.model[l][i] = 0

	def printModel(self):
		for l in Model.alphabet:
			line = l
			for i in Model.alphabet:
				line = line + " " + str(self.model[l][i])
			print line

	def trainModelfromDB(self, dbops):
		stime = time.time()
		dbSize = dbops.count_rows("DOMAINS")
		for i in range (1, dbSize+1):
			dom_name = dbops.retrieve_domain_name(i)
			label = dbops.retrieve_ping_result(i)
			self.updateModel(dom_name, label)
		print "Training took " + str(time.time()-stime) + " sec"

	def updateModel(self, string, label):
		inc = 0
		if (label==1):
			inc = 1
		elif (label==0):
			inc = -1
		for i in range(1, len(string)):
			self.model[string[i-1]][string[i]] += inc

	def predict(self, name):
		lean = 0
		for i in range(1, len(name)):
			lean += self.model[name[i-1]][name[i]]
		if (lean > 0) :
			return 1
		else:
			return 0
