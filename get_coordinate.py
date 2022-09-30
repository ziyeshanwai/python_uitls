import cv2
import os
import numpy as np
import json


def load_json(json_file):
    """
    load json file
    :param json_file: json 文件路径
    :return:
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def un_normalize(data, w, h):
    data[:, 0] = (data[:, 0] + 1) * w / 2
    data[:, 1] = (-data[:, 1] + 1) * h / 2
    return data


def write_json(json_file, data):
    with open(json_file, 'w') as f:
        json.dump(data, f)
        print("write {}".format(json_file))


def draw_line(mask, line_coors):
    line_thickness = 2
    for i in range(0, line_coors.shape[0] - 1):
        p1 = (round(line_coors[i][0]), round(line_coors[i][1]))
        p2 = (round(line_coors[i + 1][0]), round(line_coors[i + 1][1]))
        mask = cv2.line(mask, p1, p2, (0, 255, 0), thickness=line_thickness)
    return mask

def draw_circle(mask, line_coors):
    line_thickness = 2
    for i in range(0, line_coors.shape[0]):
        p1 = (round(line_coors[i][0]), round(line_coors[i][1]))
        mask = cv2.circle(mask, p1, radius=1, color=(0, 255, 0), thickness=line_thickness)
    return mask


if __name__ == "__main__":
    width = 960
    height = 1280
    img_root = r""
    img = cv2.imread(os.path.join(img_root, "0005907_c2_contour.jpg"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 129, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour_coor_list = []
    for i in range(1, len(contours)):
        tmp = contours[i].flatten()
        contour_coor_list.extend(tmp)
    print(len(contour_coor_list))
    tmp = np.array(contour_coor_list).reshape(-1, 2) * 1.0
    print(tmp)
    tmp[:, 0] = tmp[:, 0] / float(width)
    tmp[:, 1] = tmp[:, 1] / float(height)
    print(tmp)
    contour_dict = dict()
    contour_dict["contour"] = tmp.tolist()
    write_json(os.path.join(img_root, "c2.json"), contour_dict)
    # print("contours is {}".format(contours))
    # print("contours length is {}".format(len(contours)))
    # mask = np.zeros((height, width, 3), np.uint8)
    # contour = draw_circle(mask, tmp)
    # res = cv2.drawContours(tmp, contours, -1, (250, 255, 255), 1)
    # cv2.namedWindow("contour")
    # cv2.imshow("contour", contour)
    # cv2.waitKey(0)