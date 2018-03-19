import NiceDeviceConn
import csv


def dataExtractor(data):
	data = data.replace("[","")
	data = data.replace("]","")
	return data

def refExtractor(data):
	if data.find(","):
		data = data.replace(",","")
	data = data.replace('"',"")
	return data

def saleOrder(niceConn, taxDetails, fromDate, toDate):


	search_ids, saleOrderProgress =  niceConn.readData("sale.order", searchFields=[ '|', '|', ('state', '=', "progress"), ('state', '=', "done"), ('state', '=', "shipping_except"), ('date_order', '>=', fromDate), ('date_order', '<=', toDate)], readFields=["name", "client_order_ref","order_line", "date_order", "partner_id", "amount_total"])
	print "Number of SaleOrder Between (",fromDate,"to",toDate,")=",len(saleOrderProgress)

	_, saleLines = niceConn.readData("sale.order.line", searchFields=[("order_id", "=",  search_ids)], readFields=["order_id", "name", "product_uom_qty", "discount", "extra_discount", "additional_discount", "tax_id", "price_unit", "price_subtotal"])
	print "Number of SaleOrderLines Between (",fromDate,"to",toDate,")=",len(saleLines)


	field = ["Sale Order", "Date of order", "reference", "Customer", "Product", "Quantity", "Discount", "Additional Discount", "Scheme Discount", "Taxes", "Tax Desc", "Unit Price", "Sub Total", "Total"]

	rows = []
	rowValues = []
	taxes = []
	tempValues = []

	for saleOrder in saleOrderProgress:
		for saleLine in saleLines:
			if saleOrder["id"] == saleLine["order_id"][0]:
				if saleLine["tax_id"]:
					for tax in saleLine["tax_id"]:
						for taxDetail in taxDetails:
							if taxDetail["id"] == tax:
								taxes.append(taxDetail["name"])
				# print invoice["partner_id"][1]
				rowValues.append(saleOrder["name"])
				rowValues.append(str(saleOrder["date_order"].split(" ")[0]))
				if saleOrder["client_order_ref"] != False:
					rowValues.append('"'+refExtractor(saleOrder["client_order_ref"])+'"')
				else:
					rowValues.append('""')
				rowValues.append(str(dataExtractor(saleOrder["partner_id"][1].split(" ")[0])))
				rowValues.append(str(dataExtractor(saleLine["name"].split(" ")[0])))
				rowValues.append(str(saleLine["product_uom_qty"]))
				rowValues.append(str(saleLine["discount"]))
				rowValues.append(str(saleLine["extra_discount"]))
				rowValues.append(str(saleLine["additional_discount"]))
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
				rowValues.append(str(saleLine["price_unit"]))
				rowValues.append(str(saleLine["price_subtotal"]))
				rowValues.append(str(saleOrder["amount_total"]))
				rows.append(rowValues)
				rowValues = []
				taxes = []
				

	with open("ODOOORD.csv", 'w') as csvfile:
	    csvwriter = csv.writer(csvfile)

	    csvwriter.writerow(field)
	    csvwriter.writerows(rows)

	print "Sale Order Completed"

