import csv
import os
import xmlrpclib
import base64
import re
username = 'admin' #the user
pwd = 'admin'      #the password of the user
dbname = 'Odoo_back'

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://18.221.67.228:8069//xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://18.221.67.228:8069//xmlrpc/object')


sequence = 0
with open('uom.csv', 'rb') as customer_file:
    customer_datas = csv.reader(customer_file, delimiter=',', quotechar='"')
    for row in customer_datas:
        if sequence==0:
            sequence+=1
            continue
        cat_id1 = sock.execute(dbname, uid, pwd, 'product.uom.categ', 'search', [('name', '=', row[1])])
       
        if cat_id1:
            cat_read = sock.execute(dbname, uid, pwd, 'product.uom.categ', 'read', cat_id1,['name'])
            if cat_read[0]["name"] == row[1]:
                cat_id = cat_id1[0]
                print "Cat_name = ", cat_read[0]["name"]
        elif not cat_id1:
            print ".........................Categ Not Found........"
            cat_id = sock.execute(dbname, uid, pwd, 'product.uom.categ', 'create', {'name': row[1]})


        values = {
            'name': row[0],
            'category_id': cat_id,
            'uom_type': row[2],
            'factor_inv': float(row[3]),
            'rounding': row[4],
        }
        sequence += 1
        uom_id = sock.execute(dbname, uid, pwd, 'product.uom', 'search', [
            ('name', '=', values['name']), ('category_id', '=', cat_id)])
        # uom_read = sock.execute(dbname, uid, pwd, 'product.uom', 'read', uom_id, ["name"])
        if not uom_id:
            uom_id = sock.execute(dbname, uid, pwd, 'product.uom', 'create', values)
        print "Name = ", uom_id
