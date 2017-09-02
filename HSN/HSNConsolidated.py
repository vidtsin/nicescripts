import NiceDeviceConn
import csv
import time

niceConn = NiceDeviceConn.niceDevices("admin", "admin", "Odoo_back", "http://localhost:8069/xmlrpc")

hsnDatas = niceConn.readData("hs.code", readFields=["code"])
print len(hsnDatas)

tempDetail = []

with open("HSNReportWithUnTaxAmt_Chennai.csv", "rb") as csvReader:
	hsnDetails = csv.reader(csvReader, delimiter=',', quotechar='"')
	for hsnDetail in hsnDetails:
		tempDetail.append(hsnDetail)

hsnDetails = tempDetail

sequence = 1
totalHsnQuan = 0
totalHsnIgst = 0
totalHsnCgst = 0
totalHsnSgst = 0
totalHsnSumTotal = 0
totalHsnTaxedTotal = 0
hsnConsolidateSum = []
hsnConsolidateReport = []
category = False


for hsnData in hsnDatas:
	for hsnDetail in hsnDetails:
		if sequence == 1:
			sequence += 1
			continue

		if hsnData["code"][0:4] == hsnDetail[0][0:4]:
			category = hsnDetail[9].split("/")[2]
			totalHsnQuan += float(hsnDetail[3])
			totalHsnSumTotal += float(hsnDetail[4])
			totalHsnIgst += float(hsnDetail[5])
			totalHsnSgst += float(hsnDetail[6])
			totalHsnCgst += float(hsnDetail[7])
			totalHsnTaxedTotal += float(hsnDetail[8])
		sequence += 1
	if totalHsnQuan:
		hsnConsolidateSum.append(hsnData["code"][0:4])
		hsnConsolidateSum.append(category)
		hsnConsolidateSum.append(totalHsnQuan)
		hsnConsolidateSum.append(totalHsnSumTotal)
		hsnConsolidateSum.append(totalHsnIgst)
		hsnConsolidateSum.append(totalHsnSgst)
		hsnConsolidateSum.append(totalHsnCgst)
		hsnConsolidateSum.append(totalHsnTaxedTotal)
		print "HsnDetails = ",hsnData["code"][0:4],"Amount = ",totalHsnSumTotal
		hsnConsolidateReport.append(hsnConsolidateSum)
	
	sequence = 1
	totalHsnQuan = 0
	totalHsnIgst = 0
	totalHsnCgst = 0
	totalHsnSgst = 0
	totalHsnSumTotal = 0
	totalHsnTaxedTotal = 0
	category = False
	hsnConsolidateSum = []


fields = ["Hsn", "Category", "Quantity", "Untaxed Amount", "Igst", "Sgst", "Cgst", "Taxed Amount"]

with open("HsnConsolidted_Chennai.csv", "w") as csvFile:

	csvWrite = csv.writer(csvFile)

	csvWrite.writerow(fields)
	csvWrite.writerows(hsnConsolidateReport)
