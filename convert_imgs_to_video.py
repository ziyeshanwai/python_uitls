import os
import cv2
import numpy as np



def img_rotate(src, angel):
    """逆时针旋转图像任意角度

    Args:
        src (np.array): [原始图像]
        angel (int): [逆时针旋转的角度]

    Returns:
        [array]: [旋转后的图像]
    """
    h,w = src.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angel, 1.0)
    # 调整旋转后的图像长宽
    rotated_h = int((w * np.abs(M[0,1]) + (h * np.abs(M[0,0]))))
    rotated_w = int((h * np.abs(M[0,1]) + (w * np.abs(M[0,0]))))
    M[0,2] += (rotated_w - w) // 2
    M[1,2] += (rotated_h - h) // 2
    # 旋转图像
    rotated_img = cv2.warpAffine(src, M, (rotated_w,rotated_h))

    return rotated_img


if __name__ == "__main__":

    img_root = r"./"
    images_path = os.path.join(img_root, "FrontCamera")
    name = "FrontCamera"
    fps = 40    # 保存视频的FPS，可以适当调整
    # 可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    shape = (int(3088/4), int(2064/4))
    # shape = (1920, 1280)
    videoWriter = cv2.VideoWriter(os.path.join(img_root, '{}.mp4'.format(name)), fourcc, fps, (shape[1], shape[0]))  # 最后一个是保存图片的尺寸
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
        frame = img_rotate(frame, 90)
        #cv2.imshow("test", frame)
        #cv2.waitKey(0)
        videoWriter.write(frame)
        if i % 100 == 0:
            print("process {}".format(img_file))
    videoWriter.release()
