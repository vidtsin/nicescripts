import NiceDeviceConn
import xlsxwriter

niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Production", "http://54.201.242.197:8069/xmlrpc")

invoices =  niceConn.readData("account.invoice", searchFields=[("state","=","open")], readFields=["invoice_line", "partner_id", "date_invoice", "number", "origin", "amount_tax"])
print len(invoices)

invoiceLines = niceConn.readData("account.invoice.line",  readFields=["invoice_id", "display_name", "quantity", "discount", "price_unit", "price_subtotal"])
print len(invoiceLines)

stockPicking = niceConn.readData("stock.picking", readFields=["origin", "name"])

file = xlsxwriter.Workbook("invoiceReport.csv")
sheet = file.add_worksheet()

col = 0
for i in ["Invoice No", "Ref Doc", "Name", "Invoice Date","Product", "Qty", "Discount" ,"Unit Price", "Sub Total", "Total"]:
	sheet.write(1, col, i)
	col += 1

row = 3
col = 0

for invoice in invoices:
	for invoiceLine in invoiceLines:
		if invoice["id"] == invoiceLine["invoice_id"][0]:
			print invoice["partner_id"][1]
			sheet.write(row, col, invoice["number"])
			sheet.write(row, col+1, invoice["origin"])
			sheet.write(row, col+2, invoice["partner_id"][1])
			sheet.write(row, col+3, invoice["date_invoice"])
			sheet.write(row, col+4, str(invoiceLine["display_name"].split(" ")[0]))
			sheet.write(row, col+5, invoiceLine["quantity"])
			sheet.write(row, col+6, invoiceLine["discount"])
			sheet.write(row, col+7, invoiceLine["price_unit"])
			sheet.write(row, col+8, invoiceLine["price_subtotal"])
			col = 0
			row += 1

file.close()
print "completed"