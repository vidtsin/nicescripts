import xmlrpclib
import time

class niceDevices():

	def __init__(self, userName, password, dbName, url):

		self.dbName = dbName
		self.password = password
		self.userName = userName

		serverConn = self.serverProxy(self.urlFormat(url, "/common"))
		self.loginId = serverConn.login(dbName, userName, password)
		self.serverAcess = self.serverProxy(self.urlFormat(url, "/object"))


	def serverProxy(self, url):
		
		serverConn = xmlrpclib.ServerProxy(url)
		return serverConn

	def urlFormat(self, url, urlExtension):
		
		formatExtension = '{}'+str(urlExtension)
		formattedUrl = formatExtension.format(url)
		print "URL = "+str(formattedUrl)
		return formattedUrl

	def searchData(self, model, fields):

		# print "model = "+str(model)
		# print "fields = "+str(fields)
		# print "id = "+str(self.loginId)
		searchId = self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "search", fields)
		return searchId 

	def readData(self, model,  searchFields=[], readFields=[]):

		searchId = self.searchData(model, searchFields)
		# print searchId
		getData = self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "read", searchId, readFields)
		return getData

	def deleteData(self, model, fields=None):

		self.serverAcess.execute(self.dbName, self.loginId, self.password, model, 'unlink', fields)


	def updateData(self, model, id, fields):

		return self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "write", id, fields)

	def createData(self, model, data):

		self.serverAcess.execute(self.dbName, self.loginId, self.password, model, "create", data)