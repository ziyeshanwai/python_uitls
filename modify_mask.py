import bpy
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

def write_json(json_file, data):
    with open(json_file, 'w') as f:
        json.dump(data, f)
        print("write {}".format(json_file))


if __name__ == "__main__":
    json_path = os.path.join(r"D:\unreal_projects\ue51mh\Plugins\MetaHuman\Content\MeshFitting\Template", "fitting_masks.json")
    output_path = os.path.join(r"D:\unreal_projects\ue51mh\Plugins\MetaHuman\Content\MeshFitting\Template", "fitting_masks2.json")
    json_data = load_json(json_path)
    mask = []
    ob  = bpy.data.objects["mean"]
    for i in range(0, len(ob.data.vertices)):
        if ob.data.vertices[i].select:
            mask.append([i, 1])
        else:
            mask.append([i, 0])
    json_data["custom"] = mask
    write_json(output_path, json_data)