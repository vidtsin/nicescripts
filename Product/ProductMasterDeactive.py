import NiceDeviceConn



def Conn():
	niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Production", "http://54.201.242.197:8069/xmlrpc")

	products =  niceConn.readData("product.template", searchFields=[("product_brand_id","=","Purchase"),("sale_ok","=",False),("active","=", True)], readFields=["name", "active"])

	print len(products)


	for product in products:
		print product["name"]+","+str(product["id"]) +"="+str(product["active"]) 
		niceConn.updateData("product.template", product["id"], {"active":False})

try:
	Conn()
except:
	print "exception"
	Conn()