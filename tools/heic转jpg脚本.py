# coding = 'utf-8'
import os

path = 'C:\\Users\\李志卿\\1\\HEIC'
os.chdir(path)
print(os.listdir(path))
for i in os.listdir(path):
    prefix = i.split('.')[0]
    os.rename(i, prefix+'.jpg')
