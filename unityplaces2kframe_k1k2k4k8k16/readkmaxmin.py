import os
import xlrd


for file in os.listdir(os.getcwd()):
    if not file.endswith('.xls'):
        continue
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheets()[0]
    maxv, minv = 0, 1
    for i in range(2, sheet.ncols):
        for j in range(2, sheet.nrows):
            maxv = max(maxv, round(float(sheet.cell(j, i).value), 3))
            minv = min(minv, round(float(sheet.cell(j, i).value), 3))
    print(file, ',', 'k=1:', round(float(sheet.cell(1, 17).value), 3), 'max:', maxv, 'min:', minv)

