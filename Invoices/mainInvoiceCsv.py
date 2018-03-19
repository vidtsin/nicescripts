import NiceDeviceConn
import csv

def dataExtractor(data):
	data = data.replace("[","")
	data = data.replace("]","")
	return data

niceConn = NiceDeviceConn.niceDevices("admin", "admin123", "production", "http://188.42.96.102:8069/xmlrpc")

invoices =  niceConn.readData("account.invoice", searchFields=[("state","=","open"), ("company_id", "=", 1),("date_invoice", ">=", "2017-08-01"), ("date_invoice", "<=", "2017-08-31")], readFields=["invoice_line", "partner_id", "date_invoice", "number", "origin", "amount_total"])
print "invoices = ",len(invoices)

invoiceLines = niceConn.readData("account.invoice.line", readFields=["invoice_id", "display_name", "quantity", "discount", "price_unit", "price_subtotal", "invoice_line_tax_id"])
print len(invoiceLines)

stockPickings = niceConn.readData("stock.picking", readFields=["origin", "name"])
print len(stockPickings)

taxDetails = niceConn.readData("account.tax", readFields=["name", "amount"])
print "Taxes = ", len(taxDetails)

for invoice in invoices:
	for stockPicking in stockPickings:
		if invoice["origin"] == stockPicking["name"]:
			invoice["sale_order"] = stockPicking["origin"]

print len(invoices)


field =  ["Invoice No", "Sale Order","Ref Doc", "Name", "Invoice Date","Product", "Qty", "Discount" , "Taxes", "Tax Desc", "Unit Price", "Sub Total", "Total"]

# col = 0
# for i in:
# 	sheet.write(1, col, i)
# 	col += 1

# row = 3
# col = 0

rows = []
rowValues = []
taxes = []

for invoice in invoices:
	for invoiceLine in invoiceLines:
		if invoice["id"] == invoiceLine["invoice_id"][0]:
			if invoiceLine["invoice_line_tax_id"]:
				for tax in invoiceLine["invoice_line_tax_id"]:
					for taxDetail in taxDetails:
						if taxDetail["id"] == tax:
							taxes.append(taxDetail["name"])
			rowValues.append(invoice["number"])
			if "sale_order" not in invoice.keys():
				rowValues.append("")
			else:
				rowValues.append(invoice["sale_order"])
			rowValues.append(invoice["origin"])
			rowValues.append(dataExtractor(invoice["partner_id"][1].split(" ")[0]))
			rowValues.append(invoice["date_invoice"])
			rowValues.append(dataExtractor(str(invoiceLine["display_name"].split(" ")[0])))
			rowValues.append(invoiceLine["quantity"])
			rowValues.append(invoiceLine["discount"])
			if taxes:
				taxes = taxes[0].split("@")
				if taxes[0] == "CGST" or taxes[0] == "SGST":
					rowValues.append(float(taxes[1]) * 2)
					rowValues.append("Local")
				else:
					rowValues.append(float(taxes[1]))
					rowValues.append("Inter")
			else:
				rowValues.append(0)
				rowValues.append("No tax")	
			rowValues.append(invoiceLine["price_unit"])
			rowValues.append(invoiceLine["price_subtotal"])
			rowValues.append(invoice["amount_total"])
			# print rowValues
			rows.append(rowValues)
			rowValues = []
			taxes = []
			# print taxes

 
with open("InvoiceTest_Kochi.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(field)
    csvwriter.writerows(rows)
# file.close()
print "completed"