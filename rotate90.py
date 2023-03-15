# _*_ coding: utf-8 _*_
# @FileName:rotate90
# @Date:2023-03-09:10:
# @Auther: liyou wang
# @Contact: matrix2@foxmail.com

import os
import numpy as np
from scipy.spatial.transform import Rotation as R
import argparse


class Rotation90Mesh:
    def __init__(self, input_dir, output_dir):
        self._input_dir = input_dir
        self._output_dir = output_dir
        self._face = None
        self._rotation_angle = 90

    @staticmethod
    def _load_obj(path):
        """Load obj file
        读取三角形和四边形的mesh
        返回vertex和face的list
        """
        if path.endswith('.obj'):
            f = open(path, 'r')
            lines = f.readlines()
            vertics = []
            faces = []
            vts = []
            for line in lines:
                if line.startswith('v') and not line.startswith('vt') and not line.startswith('vn'):
                    line_split = line.split()
                    ver = line_split[1:4]
                    ver = [float(v) for v in ver]
                    vertics.append(ver)
                else:
                    if line.startswith('f'):
                        faces.append(line)
                    if line.startswith('vt'):
                        vts.append(line)
            return vertics, faces, vts

        else:
            print('格式不正确，请检查obj格式')
            return

    @staticmethod
    def _write_obj(file_name_path, vertexs, faces, vts=[]):
        """
        write the obj file to the specific path
        file_name_path:保存的文件路径
        vertexs:顶点数组 list
        faces: 面 list
        """
        with open(file_name_path, 'w') as f:
            for v in vertexs:
                # print(v)
                f.write("v {} {} {}\n".format(v[0], v[1], v[2]))
            for uv in vts:
                f.write(uv)
            for fa in faces:
                f.write(fa)

            print("saved mesh to {}".format(file_name_path))

    def run(self):
        objs = sorted(os.listdir(self._input_dir))
        r = R.from_euler('x', self._rotation_angle, degrees=True)
        m = r.as_matrix()
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
        for ob in objs:
            v, self._face, vts = self._load_obj(os.path.join(self._input_dir, ob))
            v = m.dot(np.array(v).T).T.tolist()
            self._write_obj(os.path.join(self._output_dir, ob), v, self._face, vts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rotate Mesh 90 Degree')
    parser.add_argument('--inputdir', '-in', type=str, help='input dir')
    parser.add_argument('--outputdir', '-out', type=str, help='output dir')
    args = parser.parse_args()
    print("args is {}".format(args))
    rm90 = Rotation90Mesh(args.inputdir, args.outputdir)
    rm90.run()
