import json
import os


def load_json(json_file):
    """
    load json file
    :param json_file: json 文件路径
    :return:
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def write_json(json_file, data):
    with open(json_file, 'w') as f:
        json.dump(data, f)
        print("write {}".format(json_file))


if __name__ == "__main__":
    data_root = r""
    source1_json = r"xx.json"
    source2_json = r"xx.json"
    target_json = r"xxx.json"
    data1 = load_json(os.path.join(data_root, source1_json))
    data2 = load_json(os.path.join(data_root, source2_json))
    s_perframe = 1/24
    target_data = data1[0:259].copy()
    frame_index = 259
    for i in range(0, len(data2)):
        tmp = data2[i].copy()
        tmp['frameIndex'] = frame_index + i
        tmp['time'] = (frame_index + i) * s_perframe
        target_data.append(tmp)
    write_json(os.path.join(data_root, target_json), target_data)

