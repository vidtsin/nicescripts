import NiceDeviceConn

niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Odoo_back", "http://localhost:8069/xmlrpc")


customers = niceConn.readData("res.partner", searchFields = [("is_company", "=", True)], readFields = ["name","gst_no", "gst_reg", "country_base_gst_type", "gst_category", "country_id", "state_id"])
print len(customers)


customerTypes = niceConn.readData("sale.order.type", searchFields = [("company_id", "=", 1)], readFields=["name"])

typeCustomer = {}

for customerType in customerTypes:
	typeCustomer[customerType["name"]] = customerType["id"]
 
subTypes = niceConn.readData("sale.order.sub.type", searchFields = [("company_id", "=", 1)], readFields=["name"])


local = []
interstate = []
localCons = []
interstateCons = []
for subType in subTypes:
	if subType["name"] == "Regular Interstate":
		interstate.append(subType["id"])
	elif subType["name"] == "Regular Local":
		local.append(subType["id"])
	elif subType["name"] == "Local Consumers":
		localCons.append(subType["id"])
	elif subType["name"] == "Interstate Consumers":
		interstateCons.append(subType["id"])

local = (6, 0, local)
interstate = (6, 0, interstate)
localCons = (6, 0, localCons)
interstateCons = (6, 0, interstateCons)


local = [local]
interstate = [interstate]
localCons  = [localCons]
interstateCons = [interstateCons]
count = 0
for customer in customers:
	count += 1
	print customer["name"], count
	if customer["country_base_gst_type"]:
		if customer["country_base_gst_type"] =="national" and customer["gst_category"] == "igst":
			if customer["gst_reg"] == "registered" :
				niceConn.updateData("res.partner", customer["id"], {"sale_type":typeCustomer["Head Office B2B"]})
			elif customer["gst_reg"] == "unregistered":
				niceConn.updateData("res.partner", customer["id"], {"sale_type":typeCustomer["Head Office B2C"]})

	# if customer["gst_category"] == "gst" and customer["gst_reg"] == "registered":
	# 	print customer["name"], " local = ", local
	# 	niceConn.updateData("res.partner", customer["id"], {"sale_sub_type_id":local})
	# elif customer["gst_category"] == "igst" and customer["gst_reg"] == "registered":
	# 	print customer["name"], " interstate = ", interstate
	# 	niceConn.updateData("res.partner", customer["id"], {"sale_sub_type_id":interstate})
	# elif customer["gst_category"] == "gst" and customer["gst_reg"] == "unregistered":
	# 	print customer["name"], " localCons = ", localCons
	# 	niceConn.updateData("res.partner", customer["id"], {"sale_sub_type_id":localCons})
	# elif customer["gst_category"] == "igst" and customer["gst_reg"] == "unregistered":
	# 	print customer["name"], " interstateCons = ", interstateCons
	# 	niceConn.updateData("res.partner", customer["id"], {"sale_sub_type_id":interstateCons})	