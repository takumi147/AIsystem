import xlrd
import os


def get_max_value(filename):
    # 打开Excel文件
    workbook = xlrd.open_workbook(filename)
    
    # 选择第一个工作表
    worksheet = workbook.sheet_by_index(0)
    
    # 初始化最大值为None
    max_value = 0
    max_value_col = 0
    max_value_row = 0

    # 遍历每个单元格
    for row in range(worksheet.nrows):
        for col in range(worksheet.ncols):
            cell_value = worksheet.cell_value(row, col)
            
            # 检查单元格是否为数值类型
            if isinstance(cell_value, float) or isinstance(cell_value, int):
                # 如果最大值为None或者当前单元格的值大于最大值，则更新最大值
                if cell_value < 1 and cell_value > max_value:
                    max_value = cell_value
                    max_value_col = col-1
                    max_value_row = row
    
    return max_value, max_value_col, max_value_row

# 测试代码
for file in os.listdir(os.getcwd()):
    if file.endswith('.xls'):
        max_value, max_value_col, max_value_row = get_max_value(file)
        print(f"{file}中最大值为:", max_value, f'此时a为{max_value_row}, b为{max_value_col}')
