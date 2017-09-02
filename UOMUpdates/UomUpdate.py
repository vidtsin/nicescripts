import NiceDeviceConn
import xlsxwriter


niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Odoo_back", "http://localhost:8069/xmlrpc")

uoms =  niceConn.readData("product.uom")

file = xlsxwriter.Workbook("uomDetails.xlsx")
sheet = file.add_worksheet()

col = 0
for i in ["name", "UOM Category", "UOM Type", "Ratio", "Active", "Rounding"]:
	sheet.write(1, col, i)
	col += 1

row = 3
col = 0

for uom in uoms:
	sheet.write(row, 0, uom["name"])
	sheet.write(row, 1, uom["category_id"][1])
	sheet.write(row, 2, uom["uom_type"])
	if  uom["uom_type"] =="bigger":
		sheet.write(row, 3, uom["factor_inv"])
	elif  uom["uom_type"] =="smaller":
		sheet.write(row, 3, uom["factor"])
	else:
		sheet.write(row, 3, 0)
	sheet.write(row, 4, uom["active"])
	sheet.write(row, 5, uom["rounding"])

	row += 1

file.close()
print "completed"