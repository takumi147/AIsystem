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
    row0 = ('', 'β', '8/16', '9/16', '10/16', '11/16', '12/16', '13/16', '14/16', '15/16', '1' )
    col0 = ('k=2', 'k=4', 'k=8', 'k=16')
    col1 = ('a=1/2', 'a=1',
            'a=2/4','a=3/4','a=1',
            'a=4/8','a=5/8','a=6/8','a=7/8','a=1',
            'a=8/16','a=9/16','a=10/16','a=11/16','a=12/16','a=13/16','a=14/16','a=15/16','a=1',
            )

    # write default format
    for i in range(0,11):
        sheet.write(0, i, row0[i])
    for i in range(0,19):
        sheet.write(i+1, 1, col1[i])
    sheet.write(1, 0, col0[0])
    sheet.write(3, 0, col0[1])
    sheet.write(6, 0, col0[2])
    sheet.write(11, 0, col0[3])

    # create a dic to give results the position(row) to write
    dic = {(2, 1): 1, (2, 2): 2, (4, 2): 3, (4, 3): 4, (4, 4): 5,
        (8, 4): 6, (8, 5): 7, (8, 6): 8, (8, 7): 9, (8, 8): 10, 
        (16, 8): 11,  (16, 9): 12, (16, 10): 13, (16, 11): 14, (16, 12): 15, (16, 13): 16,
        (16, 14): 17, (16, 15): 18, (16, 16): 19,}

    # write k-frame results
    for result in results:
        k = result[0]
        a = result[1]
        sheet.write(dic[(k, a)], result[2]-6, result[3])
    
    # save excel file
    name = 'k-frame.xls'
    book.save(name)


if __name__ == '__main__':
    write_excel([[2,2,8,0],])