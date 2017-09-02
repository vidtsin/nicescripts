import NiceDeviceConn

niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Odoo_back", "http://localhost:8069/xmlrpc")

customers = niceConn.readData("res.partner", searchFields = [("is_company", "=", True)], readFields = ["gst_no"])

print len(customers)
count = 0
for customer in customers:
	if customer["gst_no"]:
		print str(customer["gst_no"]) +" and "+str(customer["id"])
		niceConn.updateData("res.partner", customer["id"],{"gst_reg":"registered"})
	elif not customer["gst_no"]:
		niceConn.updateData("res.partner", customer["id"],{"gst_reg":"unregistered"})
	count += 1
	print count 