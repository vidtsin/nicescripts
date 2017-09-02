import NiceDeviceConn
import csv

niceConn = NiceDeviceConn.niceDevices("adminsale331", "adminsale331", "Production", "http://54.201.242.197:8069/xmlrpc")

invoices =  niceConn.readData("account.invoice", searchFields=[("state","=","open"),("company_id", "=", 5),("date_invoice", ">=", "2017-07-01"), ("date_invoice", "<=", "2017-07-31"), ("number", "!=", "SCNJ/2017/0001"), ("number", "!=", "SAJ-B-321/2017/0053"), ("number", "!=", "SAJ-321-B-00164")], readFields=["number"])
print "invoices = ", len(invoices)

productTemplates = niceConn.readData("product.template", readFields=["hs_code_id", "categ_id"])

productDatas = niceConn.readData("product.product", readFields=["default_code", "name_template", "product_tmpl_id"])
print "productDatas = ", len(productDatas)

taxDetails = niceConn.readData("account.tax", readFields=["name", "amount"])
print "Taxes = ", len(taxDetails)

invoiceLines = niceConn.readData("account.invoice.line",  searchFields=[("company_id", "=", 5)], readFields=["invoice_id" , "product_id", "quantity", "discount", "price_unit", "price_subtotal", "invoice_line_tax_id"])
print "invoiceLines = ", len(invoiceLines)
# print invoiceLines

tempInvoice = []
for invoice in invoices:
	for invoiceLine in invoiceLines:
		if invoice["id"] == invoiceLine["invoice_id"][0]:
			tempInvoice.append(invoiceLine)

invoiceLines = tempInvoice
print "temp Invoice = ", len(tempInvoice)

productHS = []

for productData in productDatas:
	for productTemplate in productTemplates:
		if productData["product_tmpl_id"][0] == productTemplate["id"]:
			if productTemplate["hs_code_id"] :
				productData["hs_code"] = productTemplate["hs_code_id"][1]
				productData["categ_id"] = productTemplate["categ_id"][1]
			else:
				productData["hs_code"] = False
				productData["categ_id"] = False
			productHS.append(productData)

productDatas = productHS

totalQty = 0
product = []
products = []
totalAmount = 0
untaxedAmount = 0
priceUnit = 0
igstTotal = 0
cgstTotal = 0
sgstTotal = 0
sgst = 0
cgst = 0
igst = 0

for productData in productDatas:
	for invoice in invoiceLines:
		if productData["id"] == invoice["product_id"][0]:
			totalQty += invoice["quantity"]
			untaxedAmount += invoice["price_subtotal"]
			discountRate = round(invoice["price_unit"] - ((invoice["price_unit"] * invoice["discount"])/100), 2)
			
			if invoice["invoice_line_tax_id"]:
				for tax in invoice["invoice_line_tax_id"]:
					for taxDetail in taxDetails:
						if tax == taxDetail["id"]:
							if taxDetail["name"].startswith("SGST"):
								sgst = round((invoice["quantity"] * discountRate * taxDetail["amount"]), 2)
							elif taxDetail["name"].startswith("CGST"):
								cgst = round((invoice["quantity"] * discountRate * taxDetail["amount"]), 2)
							elif taxDetail["name"].startswith("IGST"):
								igst = round((invoice["quantity"] * discountRate * taxDetail["amount"]), 2)
			totalAmount += 	invoice["price_subtotal"] + sgst + cgst + igst
			igstTotal += igst
			cgstTotal += cgst
			sgstTotal += sgst
			sgst = 0
			cgst = 0
			igst = 0
	if totalAmount and totalQty:
		product.append(productData["hs_code"])
		product.append(productData["name_template"])
		product.append(productData["default_code"])
		product.append(totalQty)
		product.append(untaxedAmount)
		product.append(igstTotal)
		product.append(sgstTotal)
		product.append(cgstTotal)
		product.append(totalAmount)
		product.append(productData["categ_id"])
		products.append(product)
	
	product = []
	
	totalQty = 0
	totalAmount = 0
	untaxedAmount = 0
	igstTotal = 0
	cgstTotal = 0
	sgstTotal = 0
	sgst = 0
	cgst = 0
	igst = 0


field =  ["HSN" , "NAME", "P CODE", "TOTAL QUANTITY", "UNTAXED TOTAL", "IGST", "SGST", "CGST", "TAXED TOTAL"]

with open("HSNReportWithUnTaxAmt_Chennai.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    csvwriter.writerow(field)
    csvwriter.writerows(products)
print "completed"

