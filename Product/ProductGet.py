import NiceDeviceConn

niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Odoo_back", "http://localhost:8069/xmlrpc")

products =  niceConn.readData("product.template", searchFields=[("product_brand_id","=","Purchase"),("active","=", True)], readFields=["supplier_taxes_id", "name"])

for product in products:
	print product