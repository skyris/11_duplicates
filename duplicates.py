from functools import partial
import hashlib
import os
from sys import argv
import time


USE_MD5 = False


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print("time: {}".format(time.time() - start))
        return res
    return wrapper


def files_processing(base_path):
    if not os.path.exists(base_path):
        return None
    if not os.path.isdir(base_path):
        return None
    all_files = {}
    for dir_path, dir_names, file_names in os.walk(base_path):
        for file_name in file_names:
            full_path = os.path.join(dir_path, file_name)
            all_files[full_path] = md5(full_path) if USE_MD5 else (file_name, os.path.getsize(full_path))
    return all_files


def are_files_duplicates(file_path1, file_path_2):
    return md5(file_path1) == md5(file_path_2)


def md5(filename, chunksize=4096):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as file_handler:
        read_chunk = partial(file_handler.read, chunksize)
        for chunk in iter(read_chunk, b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


if __name__ == '__main__':
    if len(argv) != 2:
        print("Ввидите имя папки, внутри которой вы хотите проверить на дубликаты после 'python3 {}'".format(__file__))
        exit()
    if argv[1] == "--help":
        print("Скачайте список московских баров в формате json с сайта http://data.mos.ru/opendata/7710881420-bary.")
        print("Поместите в текущую директорию. Наберите python3 {} <имя файла> и нажмите enter.".format(__file__))
        exit()
    pass
    print(md5("/home/victor/downloads/Westworld.S01E02.720p.HDTV.x264-BATV[ettv]/"
              "Westworld.S01E02.720p.HDTV.x264-BATV[ettv].mkv"))
    # print("программе могут потребоваться повышение полномочий")
    # print("Дать права root?")
    # # TODO Повысить права
    # # TODO Вернуть прежние права?
    # file_processing("/home/victor/projects/devman/4_json")
