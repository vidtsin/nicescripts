import NiceDeviceConn
import csv

def dataExtractor(data):
	data = data.replace("[","")
	data = data.replace("]","")
	return data

def invoices(niceConn, taxDetails, fromDate, toDate):

	# search_id, invoices =  niceConn.readData("account.invoice", searchFields=[("state","=","open"), ("date_invoice", ">=", fromDate), ("date_invoice", "<=", toDate)], readFields=["invoice_line", "partner_id", "date_invoice", "number", "origin", "amount_total", "sale_order"])
	search_id, invoices =  niceConn.readData("account.invoice", searchFields=[("state","=","open"), ('number', '=', 'SAJ-321-B-05517')], readFields=["invoice_line", "partner_id", "date_invoice", "number", "origin", "amount_total", "sale_order"])
	print "Number of invoices Between (",fromDate,"to",toDate,")=",len(invoices)
	# print invoices

	_, invoiceLines = niceConn.readData("account.invoice.line", searchFields=[("invoice_id", '=', search_id)], readFields=['invoice_id', 'extra_discount', 'additional_discount','extra_discount', 'additional_discount', 'quantity', 'discount', 'display_name', 'invoice_line_tax_id', 'price_unit', 'price_subtotal', 'product_id'])
	print "Number of invoiceLines Between (",fromDate,"to",toDate,")=",len(invoiceLines)

	_, stockPickings = niceConn.readData("stock.picking", readFields=["origin", "name"])
	
	# for invoice in invoices:
	# 	for stockPicking in stockPickings:
	# 		if invoice["origin"] == stockPicking["name"]:
	# 			invoice["sale_order"] = stockPicking["origin"]


	field =  ["Invoice No", "Sale Order","Ref Doc", "Name", "Invoice Date","Product", "Qty", "Discount", "Additional Discount", "Scheme Discount", "Taxes", "Tax Desc", "Unit Price", "Sub Total", "Total"]

	rows = []
	rowValues = []
	taxes = []
	order_list = []
	order_dict = {}
	moves = ""
	reference = ""
	number = ""
	tax_particular = ""
	tax_value = 0

	for invoice in invoices:
		if invoice['sale_order']:
			order_list = tuple(invoice['sale_order'].replace(" ", "").split(','))
		# print order_list
		for invoiceLine in invoiceLines:
			if invoice["id"] == invoiceLine["invoice_id"][0]:
				prodName = dataExtractor(str(invoiceLine["display_name"].split(" ")[0])) + str(invoiceLine["additional_discount"])
				if order_dict.has_key(invoice["number"]):
					if order_dict[invoice["number"]].has_key(prodName):
						if order_dict[invoice["number"]][prodName][8] == invoiceLine["additional_discount"]:
							order_dict[invoice["number"]][prodName][5] += invoiceLine["quantity"]
							continue
				else:
					order_dict[invoice["number"]] = {}
				if invoiceLine["invoice_line_tax_id"]:
					for tax in invoiceLine["invoice_line_tax_id"]:
						for taxDetail in taxDetails:
							if taxDetail["id"] == tax:
								taxes.append(taxDetail["name"])
				if len(order_list) > 1:
					_, stockMoves = niceConn.readData("stock.move", searchFields=[('origin', 'in', tuple(order_list)), ('product_id', '=', invoiceLine['product_id'][0]), ('state', '=', 'done')], readFields=["origin", "name", "product_uom_qty", "picking_id"])
					# print "stock moves for  = "+str(stockMoves)
					moves = ""
					reference = ""
					for stockMove in stockMoves:
						if stockMove["product_uom_qty"]:
							moves = str(moves) + str(stockMove['origin']) + ">" + str(stockMove["product_uom_qty"]) + ";"
							reference = str(reference) + str(stockMove['picking_id'][1]) + ";"
					if moves.split(";"):
						if len(moves.split(";"))>2:
							moves = str(moves)
						else:
							moves = str(moves.split(";")[0].split(">")[0])
					if reference.split(";"):
						if len(reference.split(";")) > 2:
							reference = str(reference)
						else:
							reference = str(reference.replace(";", ""))
				else:
					moves = invoice["sale_order"].replace(',',';')
					reference = invoice["origin"].replace(',',';')
				# print taxes
				if taxes:
					taxes = taxes[0].split("@")
					if taxes[0] == "CGST" or taxes[0] == "SGST":
						tax_value = float(taxes[1]) * 2
						tax_particular = "Local"
					else:
						tax_value = float(taxes[1])
						tax_particular = "Inter"
				else:
					tax_value = 0
					tax_particular = "No tax"
				taxes = []
				order_dict[invoice['number']].update({prodName : [moves, reference, dataExtractor(invoice["partner_id"][1].split(" ")[0]), invoice["date_invoice"], dataExtractor(str(invoiceLine["display_name"].split(" ")[0])), invoiceLine["quantity"], invoiceLine["discount"], invoiceLine["extra_discount"], invoiceLine["additional_discount"], tax_value, tax_particular, invoiceLine["price_unit"], invoiceLine["price_subtotal"], invoice["amount_total"]]})
	# print order_dict
				
	for order in order_dict:
		for prod in order_dict[order]:
			rowValues.append(order)
			rowValues.append(order_dict[order][prod][0])
			rowValues.append(order_dict[order][prod][1])
			rowValues.append(order_dict[order][prod][2])
			rowValues.append(order_dict[order][prod][3])
			rowValues.append(order_dict[order][prod][4])
			rowValues.append(order_dict[order][prod][5])
			rowValues.append(order_dict[order][prod][6])
			rowValues.append(order_dict[order][prod][7])
			rowValues.append(order_dict[order][prod][8])
			rowValues.append(order_dict[order][prod][9])
			rowValues.append(order_dict[order][prod][10])
			rowValues.append(order_dict[order][prod][11])
			rowValues.append(order_dict[order][prod][12])
			rowValues.append(order_dict[order][prod][13])
			rows.append(rowValues)
			rowValues = []
	# print order_dict[invoice['number']]
	with open("ODOOINV.csv", 'w') as csvfile:
	    csvwriter = csv.writer(csvfile)

	    csvwriter.writerow(field)
	    csvwriter.writerows(rows)
	# file.close()
	print "Invoice Report completed"


