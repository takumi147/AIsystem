# -*- coding: utf-8 -*-
import os

"""
change jpg name to "place1_whitecane01.mp4_001.jpg"
"""


def rewrite(path):
    os.chdir(path)
    firstnum = 10000
    for file in os.listdir(os.getcwd()):
        n = int(file.split('-')[1].split('_')[0])
        firstnum = min(n, firstnum)

    for file in os.listdir(os.getcwd()):
        if file == 'classes.txt':
            os.remove(file)
            continue
        if file == os.path.basename(__file__):
            continue
        pre = file.split('-')[0].split('_')[0]
        num = file.split('-')[1].split('_')[0]
        suf = file.split('.')[-1]

        newnum = str(int(num) - int(firstnum))
        if len(newnum) == 1:
            newfile = pre + '.mp4' + '_00' + newnum + '.' + suf
        elif len(newnum) == 2:
            newfile = pre + '.mp4' + '_0' + newnum + '.' + suf
        else:
            newfile = pre + '.mp4' + '_' + newnum + '.' + suf
        os.rename(file, newfile)
        print(file, '改成了', newfile )

    
print('program start')
for i in range(1, 20):
    if i in (5, 15):
        continue
    path1 = fr'D:\夜の白杖データ\img\night{i}\test\labels'
    path2 = fr'D:\夜の白杖データ\img\night{i}\test\images'
    rewrite(path1)
    rewrite(path2)
    
print('program end')
