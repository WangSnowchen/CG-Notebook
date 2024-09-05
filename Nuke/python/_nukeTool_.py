import nuke
import os

def close_all_animation():
    selected_nodes = nuke.selectedNodes()
    for node in selected_nodes:
        knobs = node.knobs()
        for knob_name in knobs:
            knob = node[knob_name]
            knob.clearAnimated()

def rename_files(path: str, ori_name: str, replace_name: str):
    try:
        folder_path = path
        file_list = os.listdir(folder_path)
        for filename in file_list:
            if ori_name in filename:
                new_filename = filename.replace(ori_name, replace_name)
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
                print(f'Renamed: {filename} -> {new_filename}')
    except Exception as e:
        print(f'An error occurred: {e}')
# 调用示例
#rename_files('/home/wangxuechen/Documents/test', 'char_mask_right', 'char_mask_left')

