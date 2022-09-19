import cv2
import os
import argparse
import shutil


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RENAME IMAGE SEQUENCES')
    parser.add_argument('--inputdir', '-i', type=str, help='input directory')
    parser.add_argument('--outputdir', '-o', type=str, help='output directory')
    args = parser.parse_args()
    dir_in = args.inputdir
    dir_out = args.outputdir
    files = os.listdir(dir_in)
    num = 0
    for file in files:
        name, ext = os.path.splitext(file)
        shutil.copy(os.path.join(dir_in, file), os.path.join(dir_out, "{:0>4d}.jpg".format(int(name))))
        num += 1
        if num % 100 == 0:
            print("copy {} >>>> {}".format(os.path.join(dir_in, file), os.path.join(dir_out, "{:0>4d}.jpg".format(int(name)))))