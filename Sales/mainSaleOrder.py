import NiceDeviceConn
import xlsxwriter



def dataExtractor(data):
	data = data.replace("[","")
	data = data.replace("]","")
	return data

niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Production", "http://54.201.242.197:8069/xmlrpc")

saleOrderProgress =  niceConn.readData("sale.order", searchFields=[('state', '=', "progress")], readFields=["name", "order_line", "date_order", "partner_id"])

saleOrderDone =  niceConn.readData("sale.order", searchFields=[('state', '=', "done")], readFields=["name", "order_line", "date_order", "partner_id"])

for saleOrder in saleOrderDone:
	saleOrderProgress.append(saleOrder)

saleLines = niceConn.readData("sale.order.line",  readFields=["order_id", "name", "product_uom_qty", "discount", "price_unit", "price_subtotal"])

file = xlsxwriter.Workbook("saleReport.csv")
sheet = file.add_worksheet()

col = 0
for i in ["Sale Order", "Date of order","Customer", "Product", "Quantity", "Discount", "Unit Price", "Sub Total"]:
	sheet.write(1, col, i)
	col += 1

row = 3
col = 0

for saleOrder in saleOrderProgress:
	for saleLine in saleLines:
		if saleOrder["id"] == saleLine["order_id"][0]:
			# print invoice["partner_id"][1]
			sheet.write(row, col, saleOrder["name"])
			sheet.write(row, col+1, str(saleOrder["date_order"].split(" ")[0]))
			sheet.write(row, col+2, str(dataExtractor(saleOrder["partner_id"][1].split(" ")[0])))
			sheet.write(row, col+3, str(dataExtractor(saleLine["name"].split(" ")[0])))
			sheet.write(row, col+4, saleLine["product_uom_qty"])
			sheet.write(row, col+5, saleLine["discount"])
			sheet.write(row, col+6, saleLine["price_unit"])
			sheet.write(row, col+7, saleLine["price_subtotal"])
			col = 0
			row += 1

file.close()
print "completed"