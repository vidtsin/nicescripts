import NiceDeviceConn
import mainSaleOrderCSV
import datetime


def dateFormater(date):
	# print 'date = ', date 
	date = date.split("-")
	# print date
	date = date[2] + '-' + date[1] + '-' + date[0]
	# print date
	return date

niceConn = NiceDeviceConn.niceDevices("admin", "admin123", "production", "http://54.201.137.219:8069/xmlrpc")
_, taxDetails = niceConn.readData("account.tax", readFields=["name", "amount"])



# fromDate = raw_input("Enter the FromDate (DD-MM-YYYY) = ")
# fromDate = dateFormater("01-06-2017")
# toDate = raw_input("Enter the ToDate (DD-MM-YYYY) = ")
# toDate = str(datetime.datetime.now().date())

# # 
mainSaleOrderCSV.saleOrder(niceConn, taxDetails)

