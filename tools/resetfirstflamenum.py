import os


print('start')
for i in range(1, 2):
    if i in (5, 15):
        continue
    path1 = fr'C:\Users\李志卿\datasets\night{i}\test\labels'
    path2 = fr'C:\Users\李志卿\datasets\night{i}\test\images'
    for path in (path1, path2):
        os.chdir(path)
        firstflame = os.listdir(os.getcwd())[0]
        firstflamenum = firstflame.split('_')[1][:3]
        videoname = firstflame.split('_')[0]
        for txt in os.listdir(os.getcwd()):
            num = txt.split('_')[1][:3]
            newname = videoname + '_' + str(int(num) - int(firstflamenum)) + '.txt'
            os.rename(txt, newname)
print('end')
