import os
import cv2


if __name__ == "__main__":

    img_root = r"E:\blender_output"
    images_path = os.path.join(img_root, "jpgs")
    name = "jpgs"
    fps = 2    # 保存视频的FPS，可以适当调整
    # 可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # shape = (960, 1280)
    shape = (1920, 1080)
    videoWriter = cv2.VideoWriter(os.path.join(img_root, '{}.mp4'.format(name)), fourcc, fps, shape)  # 最后一个是保存图片的尺寸
    imgs = sorted(os.listdir(images_path))
    for i, img_file in enumerate(imgs):
        # if i < 38:
        #     continue
        # if i > 3060:
        #     break
        img = cv2.imread(os.path.join(images_path, img_file))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = img.T  # 取决于图片是不是倒着的
        # img = cv2.flip(img, 1)  # 需要做一次对称
        frame = cv2.resize(img, dsize=shape)
        videoWriter.write(frame)
        if i % 100 == 0:
            print("process {}".format(img_file))
    videoWriter.release()
