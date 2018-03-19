from NiceDeviceConn import niceDevices

niceConn = niceDevices("admin", "admin123", "production", "http://13.126.149.140:8069")

getSaleId = niceConn.searchData("sale.order", [("name", "in", ('SO02450','SO02309','SO02223','SO02220','SO02219','SO02215','SO02213','SO02211','SO02208','SO02095','SO02094','SO02025','SO02024','SO02003','SO01967','SO01964','SO01911','SO01910','SO01909','SO01817','SO01808','SO01800','SO01799','SO01716','SO01713','SO01679','SO01667','SO01605','SO01597','SO01595','SO01569','SO01546','SO01545','SO01541','SO01530','SO1481','SO1413','SO1399','SO1389','SO1314','SO1305','SO1303','SO1301','SO1225','SO1131','SO1125','SO1121','SO1081','SO1026','SO1022','SO954','SO953','SO927','SO926','SO925','SO849','SO846','SO840','SO837','SO782','SO709','SO708','SO607','SO605','SO532','SO531','SO530','SO522','SO521','SO354','SO286','SO213','SO212','SO182','SO001'))])
print len(getSaleId)
for sale in getSaleId:
	print sale
	print niceConn.updateData("sale.order", sale, {'partner_selling_type':'special'})