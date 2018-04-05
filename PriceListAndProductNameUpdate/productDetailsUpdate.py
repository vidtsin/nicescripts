import NiceDeviceConn
import csv
import logging


conn = NiceDeviceConn.niceDevices('admin', 'admin123', 'Odoo_back', 'http://localhost:8069/xmlrpc')

with open('UpdatedDetails.csv', 'rb') as productFile:

    productDatas = csv.reader(productFile, delimiter=',', quotechar='"')

    sequence = 0

    for productData in productDatas:

    	if sequence <= 0:
    		sequence += 1
    		continue

    	if productData[2]:
    		product = conn.readData('product.template', fields=[('id','=',productData[0].strip())])
    		if product:
    			stat = conn.updateData('product.template', product, {'name':productData[1].strip(), 'list_price':float(productData[3].strip())})
    			print "product update status "+productData[2]+" = "+str(stat)