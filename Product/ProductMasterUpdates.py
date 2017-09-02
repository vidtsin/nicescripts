import NiceDeviceConn



def Conn():
	niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Production", "http://54.201.242.197:8069/xmlrpc")

	products =  niceConn.readData("product.template", searchFields=[("product_brand_id","=","Purchase"),("sale_ok","=",True)], readFields=["name", "sale_ok"])

	print len(products)


	for product in products:
		print product["name"]+","+str(product["id"]) +"="+str(product["sale_ok"]) 
		niceConn.updateData("product.template", product["id"], {"sale_ok":False})

try:
	Conn()
except:
	print "exception"
	Conn()