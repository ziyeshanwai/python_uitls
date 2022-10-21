import os
import shutil


def loadbs(file):
   file = file
   with open(file, 'r') as f:
       lines = f.readlines()
       lines = [l.split(',')[0].split('.')[-1] for l in lines]
   return lines


if __name__ == "__main__":
    source_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "sim_simply")
    target_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bs_data_simply")
    txt = os.path.join(os.path.split(os.path.realpath(__file__))[0], "b1.txt")
    names = loadbs(txt)
    for n in names:
        if os.path.exists(os.path.join(source_dir, "CTRL_expressions_{}.obj".format(n))):
            shutil.copy(os.path.join(source_dir, "CTRL_expressions_{}.obj".format(n)), os.path.join(target_dir, "CTRL_expressions_{}.obj".format(n)))
            print("copy {}".format(os.path.join(source_dir, "CTRL_expressions_{}.obj".format(n))))