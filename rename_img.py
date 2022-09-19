import multiprocessing as mp
import os
import argparse
import shutil
import time
from functools import partial


def f(file, dir_in, dir_out):
    name, ext = os.path.splitext(file)
    shutil.copy(os.path.join(dir_in, file), os.path.join(dir_out, "{:0>4d}.jpg".format(int(name))))


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser(description='RENAME IMAGE SEQUENCES')
    parser.add_argument('--inputdir', '-i', type=str, help='input directory')
    parser.add_argument('--outputdir', '-o', type=str, help='output directory')
    args = parser.parse_args()
    dir_in = args.inputdir
    dir_out = args.outputdir
    files = os.listdir(dir_in)
    num = 0
    """
    method 1 
    """
    partial_work = partial(f, dir_in=dir_in, dir_out=dir_out)  # 提取x作为partial函数的输入变量
    with mp.Pool(processes=6) as p:
        p.map(partial_work, [file for file in files])

    """
    method 2
    """
    # for file in files:
    #     name, ext = os.path.splitext(file)
    #     shutil.copy(os.path.join(dir_in, file), os.path.join(dir_out, "{:0>4d}.jpg".format(int(name))))
    #     num += 1
    #     if num % 100 == 0:
    #         print("copy {} >>>> {}".format(os.path.join(dir_in, file), os.path.join(dir_out, "{:0>4d}.jpg".format(int(name)))))

    end = time.time()
    print("copy imgs takes {}s".format(end - start))