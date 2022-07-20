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

    data_root = r"xx"
    source = os.path.join(data_root, "xxx.json")
    data = load_json(source)
    target = []
    neutral = data[0].copy()
    time = 1 / 24 * 12
    frame_index = 0
    for i in range(0, 258):
        tmp0 = data[i].copy()
        tmp0['frameIndex'] = frame_index
        tmp0['time'] = frame_index * time
        print("--"*10)
        print(tmp0['time'])
        print(tmp0['frameIndex'])
        if i == 0:
            target.append(tmp0)
            frame_index += 1
        else:
            target.append(tmp0)
            frame_index += 1
            t = neutral.copy()
            t['frameIndex'] = frame_index
            t['time'] = frame_index * time
            print(t['time'])
            print(t['frameIndex'])
            target.append(t)
            frame_index += 1
    write_json(os.path.join(data_root, "xxxx.json"), target)
