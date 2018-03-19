import NiceDeviceConn
import mainInvoiceCsv
import mainSaleOrderCSV
import datetime


def dateFormater(date):
	# print 'date = ', date 
	date = date.split("-")
	# print date
	date = date[2] + '-' + date[1] + '-' + date[0]
	# print date
	return date

# niceConn = NiceDeviceConn.niceDevices("admin", "admin123", "Odoo_back_3", "http://localhost:8069/xmlrpc")
niceConn = NiceDeviceConn.niceDevices("admin", "admin@nice", "production", "http://13.126.149.140:8069/xmlrpc")
_, taxDetails = niceConn.readData("account.tax", readFields=["name", "amount"])



# fromDate = raw_input("Enter the FromDate (DD-MM-YYYY) = ")
fromDate = dateFormater("01-01-2018")
# toDate = raw_input("Enter the ToDate (DD-MM-YYYY) = ")
toDate = str(datetime.datetime.now().date())

# #
mainInvoiceCsv.invoices(niceConn, taxDetails, fromDate, toDate)
# mainSaleOrderCSV.saleOrder(niceConn, taxDetails, fromDate, toDate)


