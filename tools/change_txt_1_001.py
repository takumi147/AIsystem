# -*- coding: utf-8 -*-
import os

"""
change jpg name to "place1_whitecane01.mp4_001.jpg"
"""


def rewrite(path):
    os.chdir(path)
    for file in os.listdir(os.getcwd()):
        if file == 'classes.txt':
            os.remove(file)
            continue
        if file == os.path.basename(__file__):
            continue
        pre = file.split('_')[0]
        num = file.split('_')[1].split('.')[0]
        num = str(int(num) - 1)
        suf = file.split('.')[-1]

        if len(num) == 1:
            newfile = pre + '_00' + num + '.' + suf
        elif len(num) == 2:
            newfile = pre + '_0' + num + '.' + suf
        else:
            continue

        os.rename(file, newfile)
        print(file, "change to", newfile)
       

    
print('program start')

path1 = fr'D:\夜の白杖データ\night25\test\images'
# path2 = fr'C:\Users\李志卿\datasets\night{i}\test\labels'
rewrite(path1)
# rewrite(path2)
    
print('program end')
