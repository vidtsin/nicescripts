import NiceDeviceConn



def Conn():
	niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Production", "http://54.201.242.197:8069/xmlrpc")

	products =  niceConn.readData("product.template", searchFields=[("product_type","=","FG"),("active","=", True)], readFields=["name", "purchase_ok"])

	for product in products:
		print product["name"]+","+str(product["id"]) +"="+str(product["purchase_ok"]) 
		niceConn.updateData("product.template", product["id"], {"purchase_ok":False})
 
try:
	Conn()
except:
	print "exception"
	Conn()