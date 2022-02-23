import cv2
import numpy as np
import math


if __name__ == "__main__":
    fx = 819.5370121724146202
    fy = 818.2700727112376171
    cx = 645.5445138955799393
    cy = 494.2077921574597781
    k1 = -0.3307780260518115
    k2 = 0.1695746831789451
    k3 = 0.0033097231105331
    p1 = -0.0040010997791651
    p2 = -0.0488198185075656
    img_path = r""
    ori_img = cv2.imread(img_path)
    rows = ori_img.shape[0]
    cols = ori_img.shape[1]
    img = ori_img.copy()
    distorted_img = np.zeros_like(ori_img)
    for j in range(rows):
        for i in range(cols):
            # 转到相机坐标系
            x = (i - cx) / fx
            y = (j - cy) / fy
            r = x * x + y * y

            # print("{}".format(r))

            # 加入径向畸变
            xDistort = x * (1 + k1 * r + k2 * r * r + k3 * r * r * r)
            yDistort = y * (1 + k1 * r + k2 * r * r + k3 * r * r * r)

            # 添加切向
            xDistort = xDistort + (2 * p1 * x * y + p2 * (r + 2 * x * x))
            yDistort = yDistort + (p1 * (r + 2 * y * y) + 2 * p2 * x * y)

            # 再转到图像坐标系
            u = xDistort * fx + cx
            v = yDistort * fy + cy

            # 双线性插值
            u0 = math.floor(u)
            v0 = math.floor(v)
            u1 = u0 + 1
            v1 = v0 + 1

            dx = u - u0
            dy = v - v0
            weight1 = (1 - dx) * (1 - dy)
            weight2 = dx * (1 - dy)
            weight3 = (1 - dx) * dy
            weight4 = dx * dy

            if u0 >= 0 and u1 < cols and v0 >= 0 and v1 < rows:
                distorted_img[j, i, :] = (1 - dx) * (1 - dy) * img[v0, u0, :] + (1 - dx) * dy * img[v1, u0, :] + dx * (
                        1 - dy) * img[v0, u1, :] + dx * dy * img[v1, u1, :]
    distorted_img = distorted_img
    show = True
    if show:
        img_h = cv2.hconcat([ori_img, distorted_img])
        img_v = cv2.vconcat([ori_img, distorted_img])
        for i in range(0, img.shape[0], 20):
            cv2.line(img_h, (0, i), (img_h.shape[1], i), color=(0, 0, 255), thickness=1)
        for i in range(0, img.shape[1], 20):
            cv2.line(img_v, (i, 0), (i, img_v.shape[0]), color=(0, 0, 255), thickness=1)
        # cv2.namedWindow("ori image", cv2.WINDOW_NORMAL)
        # cv2.namedWindow("distorted image", cv2.WINDOW_NORMAL)
        cv2.namedWindow("diff_h", cv2.WINDOW_NORMAL)
        cv2.namedWindow("diff_v", cv2.WINDOW_NORMAL)
        cv2.imshow("diff_h", img_h)
        cv2.imshow("diff_v", img_v)
        cv2.waitKey(0)
