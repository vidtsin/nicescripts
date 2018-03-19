import NiceDeviceConn

niceConn = NiceDeviceConn.niceDevices("admin", "admin123", "Production", "http://54.201.242.197:8069/xmlrpc")

customers = niceConn.readData("res.partner", searchFields = [("is_company", "=", True)], readFields = ["name","gst_no", "gst_reg", "country_base_gst_type", "gst_category", "country_id", "state_id"])
print len(customers)

customerTypes = niceConn.readData("sale.order.type", searchFields = [("company_id", "=", 1)], readFields=["name"])
typeCustomer = {}

# country = niceConn.readData("res.country", readFields=["name"])

# print 


for customerType in customerTypes:
	typeCustomer[customerType["name"]] = customerType["id"]


for customer in customers:
	if  customer["country_id"]:
		print customer["name"] ," customer =", customer["country_id"], "state_id = ", customer["state_id"]
		if customer["country_id"][1] == "India" :
			niceConn.updateData("res.partner", customer["id"], {"country_base_gst_type":"national"})
			if customer["state_id"]:
				if customer["state_id"][1] == "Kerala":
					niceConn.updateData("res.partner", customer["id"], {"gst_category":"gst"})
				else:
					niceConn.updateData("res.partner", customer["id"], {"gst_category":"igst"})
		elif customer["country_id"][1] != "India":
			niceConn.updateData("res.partner", customer["id"], {"country_base_gst_type":"international"})

	if customer["gst_no"]:
		niceConn.updateData("res.partner", customer["id"], {"gst_reg":"registered"})
	else:
		niceConn.updateData("res.partner", customer["id"], {"gst_reg":"unregistered"})