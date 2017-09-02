import xlrd

book = xlrd.open_workbook("invoiceReport.xlsx")

print book.nsheets

first_sheet = book.sheet_by_index(0)
 
# read a row
print first_sheet.row_values(0)

cell = first_sheet.cell(0,7)

print cell.value
 
# read a row slice
# cells =  first_sheet.row_slice(rowx=4,
#                                 start_colx=0,
#                                 end_colx=7)

# print cells.value