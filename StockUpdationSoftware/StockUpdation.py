import NiceDeviceConn
from datetime import datetime
import csv

def stockUpdation():

	conn = NiceDeviceConn.niceDevices("admin", "admin123", "Odoo_back", "http://localhost:8069/xmlrpc")

	vals = {}

	vals["name"] = "StockAdjustment_"+str(datetime.now())
	vals["filter"] = "partial"

	stock_id = conn.createData("stock.inventory", vals)

	location_id = conn.readData("stock.inventory", searchFields=[("id", "=", stock_id)], readFields=["location_id"])
	# print location_id
	# print location_id[1][0]["location_id"][0]
	print stock_id

	# stock_location = conn.readData("stock.location", searchFields=[("id", "=", location_id[1][0]["location_id"][0])], readFields=["id"])
	# print stock_location
	with open("NICESTOCK.csv", "rb") as stock:
		stockDetails = csv.reader(stock, delimiter=",")
		
		
	# conn.callFunction("stock.inventory", "prepare_inventory", stock_id)

	# product_id_creation = conn.createData("stock.inventory.line", {"product_id":3036, "inventory_id":stock_id, "product_qty":10, "location_id":location_id[1][0]["location_id"][0]})
	# # print product_id_creation
	# conn.callFunction("stock.inventory", "action_done", stock_id)

stockUpdation()
