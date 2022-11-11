import os

for i in os.listdir('D:\k-frame_compute\\pre'):
    a = open('D:\k-frame_compute\\pre\\' + i).read()
    if a == '':
        print('有内奸, 是：', i)
        break
print('over')