import os

c = 0
for i in range(1, 20):
    if i in (5, 15):
        continue
    path = fr'C:\Users\李志卿\datasets\night{i}\test\labels'
    os.chdir(path)
    for file in os.listdir(path):
        if file == os.path.basename(__file__):
            pass
        word = open(file).read()
        if not word:
            c += 1
    print(f'{path}里的空label有{c}个') 
    c = 0