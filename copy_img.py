import shutil
import os


if __name__ == "__main__":

    source_dir = './c1_rot'
    target_dir = './c1'
    

    file_list = os.listdir(source_dir)

    for image in file_list:

        
        if int(image.split('.')[0]) % 20 == 0:
            shutil.copy(os.path.join(source_dir, image), os.path.join(target_dir, image))
