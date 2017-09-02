import NiceDeviceConn
import csv


niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Production", "http://54.201.242.197:8069/xmlrpc")


fields = ["name", "hs_code_id", "default_code", "product_type", "categ_id"]
products =  niceConn.readData("product.template", readFields=fields)

print len(products)
 
productList = []
productsList = []

for product in products:
	productList.append(product[fields[0]])
	if product["hs_code_id"]:
		print product["hs_code_id"]
		productList.append(product[fields[1]][1])
	else:
		productList.append(False)

	productList.append(product[fields[2]])
	if product[fields[3]]:
		productList.append(product[fields[3]][1])
	else:
		productList.append(False)
	productList.append(product[fields[4]][1])
	productsList.append(productList)
	productList = []

with open("ProductDetails.csv", 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(fields)
	csvwriter.writerows(productsList)

print "completed"