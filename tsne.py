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
    json_name = 'xx.json'
    sample_path = os.path.join(r"xxx", json_name)
    samples = load_json(sample_path)
    d = [s['outputs'] for s in samples['samples']]
    data = np.array(d, dtype=np.float32)
    tsne = TSNE(n_components=2, init='pca', random_state=501)
    x_tsne = tsne.fit_transform(data)
    x_min, x_max = np.min(x_tsne, axis=0), np.max(x_tsne, axis=0)
    norm_data = (x_tsne - x_min) / (x_max - x_min)
    # plt.plot(norm_data[:, 0], norm_data[:, 1])
    plt.scatter(norm_data[:, 0], norm_data[:, 1], marker='o')
    plt.show()
