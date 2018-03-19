from time import sleep
import NiceDeviceConn

niceConn = NiceDeviceConn.niceDevices("admin", "admin123", "production", "http://13.126.149.140:8069/xmlrpc")

with open("Special.txt", "r") as special:
	readFile = special.readlines()
	for file in readFile:
		
		readData = niceConn.searchData("product.template", fields=[("default_code", "=", file.split(" ")[0])])
		print file , readData
		if readData:
			niceConn.updateData("product.template", readData[0], {"price_list":True})