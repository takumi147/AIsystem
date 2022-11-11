import os

n = 0
c = 0
for file in os.listdir('./tru'):
    t = open('./tru/' + file).read()
    l = len(t.split('\n'))
    if l > 1:
        print(file, l)
        c += 1
    if t:
        n += len(t.split('\n'))
print(n)
print(c)