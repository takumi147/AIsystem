import os


"""
由于从roboflow导出的图片命名格式和HE用的图片命名格式不一致，导致基于roboflow
的k-frame算法并不能适用。所以需要将命名格式统一。
命名格式：roboflow--> 'video name'+ '_' +'flame number.txt'
          HE--> 'video name' + '-' + 'flame number' + '_jpg' + '.xxxxxx.txt'
"""
def rname(filename):
    new_filename = filename.split('_jpg')[0] + '.txt'
    new_filename = new_filename.replace('-', '_')
    os.rename(filename, new_filename)


if __name__ == '__main__':
    pre_path = os.path.join(os.getcwd(), 'pre')
    tru_path = os.path.join(os.getcwd(), 'tru')

    for path in (pre_path, tru_path):
        for filename in os.listdir(path):
            os.chdir(path)
            rname(filename)
    
