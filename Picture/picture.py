# picture_generation.py 图像生成
from os import path
from func_collection import read_txt


def pic_generation(pg_path, file_name):
    txt = None
    file_dir = pg_path + '\\' + file_name
    if path.exists(file_dir):
        txt = read_txt(file_dir)
    print(txt)
