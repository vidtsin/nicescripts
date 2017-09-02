import NiceDeviceConn

niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Odoo_back", "http://localhost:8069/xmlrpc")

customers = niceConn.readData("res.partner", searchFields = [("is_company", "=", True)], readFields = ["gst_no", "gst_reg", "country_base_gst_type", "gst_category"])
print len(customers)

customerTypes = niceConn.readData("sale.order.type", searchFields = [("company_id", "=", 1)], readFields=["name"])

typeCustomer = {}

for customerType in customerTypes:
	typeCustomer[customerType["name"]] = customerType["id"]
 
subTypes = niceConn.readData("sale.order.sub.type", searchFields = [("company_id", "=", 1)], readFields=["name"])

local = []
interstate = []
for subType in subTypes:
	if subType["name"] == "Regular Interstate":
		interstate.append(subType["id"])
	elif subType["name"] == "Regular Local":
		local.append(subType["id"])

print local
local = (6, 0, local)
interstate = (6, 0, interstate)

local = [local]
interstate = [interstate]

for customer in customers:
	if customer["gst_no"] and customer["gst_reg"] == "registered" :
		niceConn.updateData("res.partner", customer["id"], {"sale_type":typeCustomer["Head Office B2B"]})
	elif customer["gst_no"]:
		niceConn.updateData("res.partner", customer["id"], {"sale_type":typeCustomer["Head Office B2B"], "gst_reg":"registered"})

	if customer["country_base_gst_type"] == "national":
		print str(customer["gst_no"])+" Type = " + str(customer["country_base_gst_type"]) + " and category = "+ str(customer["gst_category"])
		if customer["gst_category"] == "gst":
			niceConn.updateData("res.partner", customer["id"], {"sale_sub_type_id":local})
		elif customer["gst_category"] == "igst":
			niceConn.updateData("res.partner", customer["id"], {"sale_sub_type_id":interstate})