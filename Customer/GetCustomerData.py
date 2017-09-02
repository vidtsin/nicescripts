import NiceDeviceConn
import csv


niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Production", "http://54.201.242.197:8069/xmlrpc")

fieldsNotInProduction = ["sale_type", "sale_sub_type_id",]

fields = ["name", "street2", "city_id", "state_id", "country_id", "country_base_gst_type", "gst_category", "gst_reg", "gst_no", "pan", "ref", "gst_credit", "disc", "nedisc", "adisc", "tdisc", "section_id", "reverse_tax", "notify_email", "deemed_export","sez", "export", "tax_exempted",  "property_account_receivable", "property_account_payable", "property_payment_term"]

customers = niceConn.readData("res.partner", searchFields = [("is_company", "=", False)],readFields = fields)

customerList = []
customersList = []

for customer in customers:
	print customer
	for field in fields:
		if customer[field]:
			if type(customer[field]) is list:
				if len(customer[field]) == 2:
					if type(customer[field][1]) is str:
						customerList.append(str(customer[field][1]))
					else:
						customerList.append(str(customer[field]))
				else:
					customerList.append(str(customer[field]))
			else:
				customerList.append(str(customer[field]))
		else:
			customerList.append(str(customer[field]))
	customersList.append(customerList)
	customerList = []

with open("ContactList.csv", 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(fields)
	csvwriter.writerows(customersList)

print "completed"