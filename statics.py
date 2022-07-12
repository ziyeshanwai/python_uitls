import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import os
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


if __name__ == "__main__":
    json_name = 'xxx.json'
    sample_path = os.path.join(r"xxx", json_name)
    samples = load_json(sample_path)
    d = [s['outputs'] for s in samples['samples']]
    data = np.array(d, dtype=np.float32)
    means = data.mean(axis=1) * 1000
    print("means is {}".format(means))
    stds = np.std(data, axis=1) * 1000
    plt.figure()
    plt.hist(means, bins=10)
    plt.title('means')
    plt.figure()
    plt.hist(stds, bins=10)
    plt.title('std')
    plt.show()