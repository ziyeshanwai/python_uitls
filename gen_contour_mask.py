import numpy as np
import cv2
import multiprocessing as mp
import os
import argparse
import time
import json
from functools import partial


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


def draw_line(mask, line_coors):
    line_thickness = 2
    for i in range(0, line_coors.shape[0] - 1):
        p1 = (round(line_coors[i][0]), round(line_coors[i][1]))
        p2 = (round(line_coors[i + 1][0]), round(line_coors[i + 1][1]))
        mask = cv2.line(mask, p1, p2, (0, 255, 0), thickness=line_thickness)
    return mask


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser(description='RENAME IMAGE SEQUENCES')
    parser.add_argument('--inputdir', '-i', type=str, help='input json directory')
    parser.add_argument('--outputdir', '-o', type=str, help='output mask directory')
    parser.add_argument('--width', '-w', type=int, help='image width')
    parser.add_argument('--height', type=int, help='image height')
    args = parser.parse_args()
    w = args.width
    h = args.height
    json_files = os.listdir(args.inputdir)
    mask = np.zeros((h, w, 3), dtype=np.uint8)
    alpha_channel = np.ones((h, w), dtype=np.uint8) * 255
    num = 0

    for file in json_files:
        name, ext = os.path.splitext(file)
        contour_data = load_json(os.path.join(args.inputdir, file))
        bottom_lip = un_normalize(np.array(contour_data["contours"]["bottomLip"]["points"]).reshape(-1, 2), w, h)
        topLip = un_normalize(np.array(contour_data["contours"]["topLip"]["points"]).reshape(-1, 2), w, h)
        # leftBottomEyelid = un_normalize(np.array(contour_data["contours"]["leftBottomEyelid"]["points"]).reshape(-1, 2),
        #                                 w, h)
        # leftTopEyelid = un_normalize(np.array(contour_data["contours"]["leftTopEyelid"]["points"]).reshape(-1, 2), w, h)
        # rightBottomEyelid = un_normalize(
        #     np.array(contour_data["contours"]["rightBottomEyelid"]["points"]).reshape(-1, 2), w, h)
        # rightTopEyelid = un_normalize(np.array(contour_data["contours"]["rightTopEyelid"]["points"]).reshape(-1, 2), w,
        #                               h)
        lower_innerlip = un_normalize(np.array(contour_data["innerLips"]["contours"]["lower"]["points"]).reshape(-1, 2),
                                      w, h)
        upper_innerlip = un_normalize(np.array(contour_data["innerLips"]["contours"]["upper"]["points"]).reshape(-1, 2),
                                      w, h)
        mask_copy = draw_line(mask.copy(), bottom_lip)
        mask_copy = draw_line(mask_copy, topLip)
        mask_copy = draw_line(mask_copy, lower_innerlip)
        mask_copy = draw_line(mask_copy, upper_innerlip)
        mask_copy = cv2.merge([mask_copy, alpha_channel])
        cv2.imwrite(os.path.join(args.outputdir, "{}.png".format(name)), mask_copy)
        num += 1
        if num % 100 == 0:
            print("process {} : {}".format(num, os.path.join(args.outputdir, "{}.png".format(name))))
    end = time.time()
    print("generate mask takes {}s".format(end - start))