import NiceDeviceConn
import csv

def dataExtractor(data):
	data = data.replace("[","")
	data = data.replace("]","")
	return data

def invoices(niceConn, taxDetails, fromDate, toDate):

	# search_id, invoices =  niceConn.readData("account.invoice", searchFields=[("state","=","open"), ("date_invoice", ">=", fromDate), ("date_invoice", "<=", toDate)], readFields=["invoice_line", "partner_id", "date_invoice", "number", "origin", "amount_total", "sale_order"])
	search_id, invoices =  niceConn.readData("account.invoice", searchFields=[("state","=","open"), ('number', '=', 'SAJ-321-B-4982')], readFields=["invoice_line", "partner_id", "date_invoice", "number", "origin", "amount_total", "sale_order"])
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
	for invoice in invoices:
		if invoice['sale_order']:
			order_list = tuple(invoice['sale_order'].replace(" ", "").split(','))
		# print order_list
		for invoiceLine in invoiceLines:
			if invoice["id"] == invoiceLine["invoice_id"][0]:
				if invoiceLine["invoice_line_tax_id"]:
					for tax in invoiceLine["invoice_line_tax_id"]:
						for taxDetail in taxDetails:
							if taxDetail["id"] == tax:
								taxes.append(taxDetail["name"])
				rowValues.append(invoice["number"])
				# if "sale_order" not in invoice.keys():
				# 	rowValues.append("")
				# else:
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
							rowValues.append(str(moves))
						else:
							rowValues.append(str(moves.split(";")[0].split(">")[0]))
					if reference.split(";"):
						if len(reference.split(";")) > 2:
							rowValues.append(str(reference))
						else:
							rowValues.append(str(reference.replace(";", "")))
				else:
					rowValues.append(invoice["sale_order"].replace(',',';'))
					rowValues.append(invoice["origin"].replace(',',';'))
				rowValues.append(dataExtractor(invoice["partner_id"][1].split(" ")[0]))
				rowValues.append(invoice["date_invoice"])
				rowValues.append(dataExtractor(str(invoiceLine["display_name"].split(" ")[0])))
				rowValues.append(invoiceLine["quantity"])
				# rowValues.append(round((((invoiceLine["quantity"]*invoiceLine["price_unit"])-invoiceLine["price_subtotal"])*100 / (invoiceLine["quantity"]*invoiceLine["price_unit"])), 2))
				rowValues.append(invoiceLine["discount"])
				rowValues.append(invoiceLine["extra_discount"])
				rowValues.append(invoiceLine["additional_discount"])
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

	 
	with open("ODOOINV.csv", 'w') as csvfile:
	    csvwriter = csv.writer(csvfile)

	    csvwriter.writerow(field)
	    csvwriter.writerows(rows)
	# file.close()
	print "Invoice Report completed"


