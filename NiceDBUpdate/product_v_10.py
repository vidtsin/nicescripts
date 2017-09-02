import csv
import os
import xmlrpclib
import base64
import re
import psycopg2

username = 'admin' #the user
pwd = 'admin'      #the password of the user
dbname = 'Odoo_back'

# Get the uid
sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

try:
    conn = psycopg2.connect("dbname='Odoo_back' user='admin' host='localhost' password='admin'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()

sequence = 0
with open('ProductTest.csv', 'rb') as product_file:
    product_datas = csv.reader(product_file, delimiter=',', quotechar='"')
    for row in product_datas:
        if sequence <= 0:
            sequence += 1
            continue
        values = {'company_id': 1, 'default_code': row[1].strip() or ''}

        hs_code_name = row[2].strip() or ''        
        hs_code_id = False
        if hs_code_name:
            hs_code_id = sock.execute(dbname, uid, pwd, 'hs.code', 'search', [('description', '=', hs_code_name), ('code', '=', hs_code_name)])
            hs_code_id = hs_code_id and hs_code_id[0]
            if not hs_code_id:
                hs_code_id = sock.execute(dbname, uid, pwd, 'hs.code', 'create', {'description': hs_code_name, 'code': hs_code_name})
        values['hs_code_id'] = hs_code_id
        
        brand_name = row[3].strip() or ''
        product_brand_id = False
        if brand_name:
            product_brand_id = sock.execute(dbname, uid, pwd, 'product.brand', 'search', [('name', '=', brand_name)])
            product_brand_id = product_brand_id and product_brand_id[0]
            if not product_brand_id:
                product_brand_id = sock.execute(dbname, uid, pwd, 'product.brand', 'create', {'name': brand_name})
        values['product_brand_id'] = product_brand_id
        values['name'] = row[4].strip()

        uom_name = row[5].strip() or ''
        uom_id = False
        if uom_name:
            uom_id = sock.execute(dbname, uid, pwd, 'product.uom', 'search', [('name', '=', uom_name)])
            uom_id = uom_id and uom_id[0]
            if not uom_id:
                print "....................................UOM Not Found.........................."
        values['uom_id'] = uom_id
        values['list_price'] = float(row[6])
        values['standard_price'] = float(row[7])
        values['specific_gravity'] = row[8]

        uom_po_name = row[9].strip() or ''
        uom_po_id = False
        if uom_po_name:
            uom_po_id = sock.execute(dbname, uid, pwd, 'product.uom', 'search', [('name', '=', uom_po_name)])
            uom_po_id = uom_po_id and uom_po_id[0]
            if not uom_po_id:
                print "....................................Purchase UOM Not Found.........................."
        values['uom_po_id'] = uom_po_id

        print "uom_po_name = ", uom_po_name 

        product_type_name = row[10].strip() or ''        
        product_type = False
        if product_type_name:
            product_type = sock.execute(dbname, uid, pwd, 'product.product.type', 'search', [('name', '=', product_type_name)])
            product_type = product_type and product_type[0]
            if not product_type:
                product_type = sock.execute(dbname, uid, pwd, 'product.product.type', 'create', {'name': product_type_name})
        values['product_type'] = product_type
        
        categ_name = row[11].strip() or ''        
        categ_id = False
        if categ_name:
            categ_id = sock.execute(dbname, uid, pwd, 'product.category', 'search', [('name', '=', categ_name)])
            categ_id = categ_id and categ_id[0]
            if not categ_id:
                categ_id = sock.execute(dbname, uid, pwd, 'product.category', 'create', {
                    'name': categ_name,
                })
        values['categ_id'] = categ_id
        if row[12] == 'N':
            values['track_all'] = False
        else:
            values['track_all'] = True

        values['type'] = 'product'
        values['produce_delay'] = row[14]



        taxes_id_names = row[15].split(',') or []
        taxes_id = []        
        for taxes_id_name in taxes_id_names:
            taxes_id_name = taxes_id_name.strip()
            tax_id = False
            if taxes_id_name:
                tax_id = sock.execute(dbname, uid, pwd, 'account.tax', 'search', [('name', '=', taxes_id_name), ("company_id","=",1)])
                tax_id = tax_id and tax_id[0]
                if not tax_id:
                    tax_id = sock.execute(dbname, uid, pwd, 'account.tax', 'create', {'name': taxes_id_name})
                taxes_id.append(tax_id)
        
        taxes_id = (6, 0, taxes_id)
        taxes_id = [taxes_id]
        values['taxes_id'] = taxes_id

        s_taxes_id_names = row[16].split(',') or []        
        supplier_taxes_id = []
        for s_taxes_id_name in s_taxes_id_names:
            s_taxes_id_name = s_taxes_id_name.strip() or ''
            tax_id = False
            if s_taxes_id_name:
                tax_id = sock.execute(dbname, uid, pwd, 'account.tax', 'search', [('name', '=', s_taxes_id_name), ("company_id","=",1)])
                tax_id = tax_id and tax_id[0]
                if not tax_id:
                    tax_id = sock.execute(dbname, uid, pwd, 'account.tax', 'create', {'name': s_taxes_id_name})
                supplier_taxes_id.append(tax_id)

        supplier_taxes_id = (6, 0, supplier_taxes_id)
        supplier_taxes_id = [supplier_taxes_id]

        values["supplier_taxes_id"] = supplier_taxes_id

        boolValue = {'1':True, '0':False}
        values['warehouse_id'] = 2
        values['valuation'] = 'real_time'
        values['property_stock_account_input'] = 275
        values['property_stock_account_output'] = 277
        values['property_account_income'] = 271
        values['property_account_expense'] = 273
        values["cost_method"] = row[28]
        values["sale_ok"] = boolValue[row[29]]
        values["purchase_ok"] = boolValue[row[30]]
        values["state"] = row[31]
        values
        sequence += 1
        product_id = sock.execute(dbname, uid, pwd, 'product.template', 'search', [
            ('hs_code_id', '=', hs_code_id),
            ('name', '=', row[4].strip())])
        print "product_id = ",product_id
        print 'default_code =', row[1].strip()
        if not product_id:
            product_id = sock.execute(dbname, uid, pwd, 'product.template', 'create', values)
            # cur.execute("""update product_template set uom_id=%s, uom_po_id=%s"""%(values['uom_id'], values['uom_po_id']))
            # conn.commit()
            print "...................create.........................", product_id, sequence
        else:
            print ">>>>>>>>>>>>>>>>>>>>>>>>.product found....................", product_id, sequence
            # product_id = sock.execute(dbname, uid, pwd, 'product.template', 'write', product_id, values)
            # cur.execute("""update product_template set uom_id=%s, uom_po_id=%s"""%(values['uom_id'], values['uom_po_id']))
            # conn.commit()


        # reorder_id = sock.execute(dbname, uid, pwd, 'stock.warehouse.orderpoint', 'search', [
        #     ('product_min_qty', '=', row[17]),
        #     ('product_max_qty', '=', row[18]),
        #     ('qty_multiple', '=', row[19])])
        # if product_id:

