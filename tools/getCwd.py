from pathlib import Path
import os

file = Path(__file__).resolve()
# this is the absolute path of this file
# print(file)
# D:\AIsystem\tools\getCwd.py
file = __file__
# d:\AIsystem\tools\getCwd.py
# but cant use .parents[0]

root = file.parents[0]
# print(root)
# D:\AIsystem\tools

# root = file.parents
# # no sence
# root = file.parents[1]
# # print(root)
# # D:\AIsystem

root = os.getcwd()
# D:\AIsystem\tools

root = Path.cwd()
# D:\AIsystem\tools

b = Path(os.path.relpath(root, Path.cwd()))
# 输出为 .
# Path(os.path.relpath(path_1, path_2))应该输出的是path_2相对path_1的相对路径