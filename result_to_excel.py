import xlwt
import os


def write_excel(results):
    """
    write the results of k-frame to excel file.
    :param results: [[k, a, b, f-score],]
    :return none
    """
    # delete previous file
    if os.path.exists('k-frame.xls'):
        os.remove('k-frame.xls')
        print('旧k-frame文件已被删除，开始计算新的k-frame！')
    # default format 
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet('k-frame result',cell_overwrite_ok=True)
    row0 = ('', 'β', '1/16', '2/16', '3/16', '4/16', '5/16', '6/16', '7/16', '8/16', '9/16', '10/16', '11/16', '12/16', '13/16', '14/16', '15/16', '1')
    col0 = ('k=1', 'k=2', 'k=4', 'k=8', 'k=16')
    col1 = ('a=1',
            'a=1/2', 'a=1',
            'a=1/4', 'a=2/4','a=3/4','a=1',
            'a=1/8','a=2/8','a=3/8','a=4/8','a=5/8','a=6/8','a=7/8','a=1',
            'a=1/16','a=2/16','a=3/16','a=4/16','a=5/16','a=6/16','a=7/16','a=8/16','a=9/16','a=10/16','a=11/16','a=12/16','a=13/16','a=14/16','a=15/16','a=1',
            )

    # write default format
    for i in range(len(row0)):
        sheet.write(0, i, row0[i])
    for i in range(len(col1)):
        sheet.write(i+1, 1, col1[i])
    sheet.write(1, 0, col0[0])
    sheet.write(2, 0, col0[1])
    sheet.write(4, 0, col0[2])
    sheet.write(8, 0, col0[3])
    sheet.write(16, 0, col0[3])

    # create a dic to give results the position(row) to write, (k, a): row
    r = 1
    dic = {}
    for i in (1, 2, 4, 8, 16):
        for j in range(1, i+1):
            dic[(i, j)] = r
            r += 1

    # write k-frame results
    for result in results:
        k = result[0]
        a = result[1]
        if k == 1:
            sheet.write(dic[(k, a)], 17, result[3])
        else:
            sheet.write(dic[(k, a)], result[2]+1, result[3])
    
    # save excel file
    name = 'k-frame.xls'
    book.save(name)


if __name__ == '__main__':
    write_excel([[2,2,8,0],])