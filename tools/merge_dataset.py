import os
import shutil

from numpy import source


def merge():
    root_path = os.getcwd()
    os.mkdir(r'merge program')
    os.mkdir(r'merge program\train')
    os.mkdir(r'merge program\train\images')
    os.mkdir(r'merge program\train\labels')
    os.mkdir(r'merge program\valid')
    os.mkdir(r'merge program\valid\images')
    os.mkdir(r'merge program\valid\labels')
    os.mkdir(r'merge program\test')
    os.mkdir(r'merge program\test\images')
    os.mkdir(r'merge program\test\labels')

    dirs = os.listdir(root_path)
    for dir in dirs:
        if not os.path.isdir(dir):
            continue
        for file in os.listdir(os.path.join(root_path, dir, 'train', 'images')):
            shutil.copy(os.path.join(root_path, dir, 'train', 'images', file), 
                os.path.join(root_path, 'merge program', 'train', 'images'))
        for file in os.listdir(os.path.join(root_path, dir, 'train', 'labels')):
            shutil.copy(os.path.join(root_path, dir, 'train', 'labels', file), 
                os.path.join(root_path, 'merge program', 'train', 'labels'))
        for file in os.listdir(os.path.join(root_path, dir, 'valid', 'images')):
            shutil.copy(os.path.join(root_path, dir, 'valid', 'images', file), 
                os.path.join(root_path, 'merge program', 'valid', 'images'))
        for file in os.listdir(os.path.join(root_path, dir, 'valid', 'labels')):
            shutil.copy(os.path.join(root_path, dir, 'valid', 'labels', file),
                os.path.join(root_path, 'merge program', 'valid', 'labels'))
        for file in os.listdir(os.path.join(root_path, dir, 'test', 'images')):
            shutil.copy(os.path.join(root_path, dir, 'test', 'images', file),
                os.path.join(root_path, 'merge program', 'test', 'images'))
        for file in os.listdir(os.path.join(root_path, dir, 'test', 'labels')):
            shutil.copy(os.path.join(root_path, dir, 'test', 'labels', file),
                os.path.join(root_path, 'merge program', 'test', 'labels'))


if __name__ == '__main__':
    merge()
        