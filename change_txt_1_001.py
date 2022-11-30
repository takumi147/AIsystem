import os


print('program start')
for file in os.listdir(os.getcwd()):
    if file == os.path.basename(__file__):
        continue
    suf = file.split('_')[-1]
    pre1 = file.split('_')[0]
    pre2 = file.split('_')[1]
    num = suf.split('.')[0]
    suf = file.split('.')[-1]
    if len(num) == 1:
        newfile = pre1 + '_' + pre2 + '_' + '00' + num + '.' + suf
    elif len(num) == 2:
        newfile = pre1 + '_' + pre2 + '_' + '0' + num + '.' + suf
    else:
        continue
    os.rename(file, newfile)
print('program end')
