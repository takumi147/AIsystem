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
        pre = file.split('.')[0] + '.mp4'
        num = file.split('_')[2].split('.')[0]
        # num = str(int(num) - 1)
        suf = file.split('.')[-1]

        if len(num) == 1:
            newfile = pre + '_00' + num + '.' + suf
        elif len(num) == 2:
            newfile = pre + '_0' + num + '.' + suf
        else:
            newfile = pre + '_' + num + '.' + suf

        os.rename(file, newfile)
        print(file, "change to", newfile)

path1 = os.getcwd()
rewrite(path1)
    
print('program end')
