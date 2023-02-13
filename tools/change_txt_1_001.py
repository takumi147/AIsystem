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
        # suf = file.split('-')[0].split('_')[0]
        # num = file.split('-')[1].split('_')[0]

        # if len(num) == 1:
        #     newfile = suf + '.mp4' + '_00' + num + '.jpg'
        # elif len(num) == 2:
        #     newfile = suf + '.mp4' + '_0' + num + '.jpg'
        # else:
        #     continue
        newfile = file[:-4] + 'txt'
        os.rename(file, newfile)

    
print('program start')
for i in range(1, 2):
    if i in (5, 15):
        continue
    path1 = fr'C:\Users\李志卿\datasets\night{i}\test\images'
    path2 = fr'C:\Users\李志卿\datasets\night{i}\test\labels'
    # rewrite(path1)
    rewrite(path2)
    
print('program end')
