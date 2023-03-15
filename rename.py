# _*_ coding: utf-8 _*_
# @FileName:rename_4d_BS
# @Date:2023-03-15:16:
# @Auther: liyou wang
# @Contact: matrix2@foxmail.com

import os
import json
import shutil
import argparse


class RenameBS:
    def __init__(self, source_dir, target_dir, configfile):
        self._source_dir = source_dir
        self._target_dir = target_dir
        self._name_mapping = self._load_json(configfile)

    @staticmethod
    def _load_json(json_file):
        """
        load json file
        :param json_file: json 文件路径
        :return:
        """
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data

    def run(self):
        source_keys = list(self._name_mapping.keys())
        target_names = list(self._name_mapping.values())
        for i, n in enumerate(source_keys):
            if os.path.exists(os.path.join(self._source_dir, n)):
                shutil.copy(os.path.join(self._source_dir, "{}".format(n)),
                            os.path.join(self._target_dir, "{}".format(target_names[i])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename obj')
    parser.add_argument('--inputdir', '-in', type=str, help='input dir')
    parser.add_argument('--outputdir', '-out', type=str, help='output dir')
    parser.add_argument('--configfile', '-config', type=str, help='output dir')
    args = parser.parse_args()
    print("args is {}".format(args))
    rn = RenameBS(args.inputdir, args.outputdir, args.configfile)
    rn.run()
