import NiceDeviceConn

niceConn = NiceDeviceConn.niceDevices("admin", "admin123", "production", "http://13.126.149.140:8069/xmlrpc")

search_id, invoices =  niceConn.readData("account.invoice", searchFields=[("number","=","SAJ-B-321/2017/0003")])

updates = niceConn.updateData("account.invoice", search_id, {'number':'SAJ-321-00004'})
print "Number of invoices Between ="+str(invoices)