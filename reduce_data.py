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
    name = "bs_6000_v2"
    source = os.path.join(data_root, "{}.solver_sample.json".format(name))
    data = load_json(source)
    target = {'sampleCount': 0, "samples":[]}
    sample_count = data['sampleCount']
    count = 0
    for i in range(0, sample_count):
        if i % 12 == 1 or i % 12 == 2 or i % 12 == 3 or i % 12 == 4 :
            continue
        else:

            target["samples"].append(data["samples"][i])
            count +=1
    target['sampleCount'] = count
       
    write_json(os.path.join(data_root, "{}_data_reduced.solver_sample.json".format(name)), target)
