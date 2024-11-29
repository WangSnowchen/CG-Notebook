import nuke
import os
import glob
import re

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


def change_stereo_file_path():
    read_nodes = [node for node in nuke.allNodes() if node.Class() == 'Read']
    for node in read_nodes:
        file_path = node['file'].value()
        new_file_path = file_path.replace('left', '%V').replace('right', '%V')
        node['file'].setValue(new_file_path)

class CameraFocalLengthManager:
    def __init__(self, compPath):
        self.compPath = compPath
        self.sequence, self.shotcode = self.get_sequence_shotcode(compPath)
        self.pathTemplate = self.create_path_template(self.sequence, self.shotcode)

    def get_sequence_shotcode(self, compPath):
        splits = os.path.basename(compPath).split("_")
        sequence = splits[0]
        shotcode = '_'.join(code for code in os.path.basename(compPath).split(".")[0].split("_")[1:-2])
        return sequence, shotcode

    def create_path_template(self, sequence, shotcode):
        return os.path.join("$proj", "pj2024cg016", "sequences", sequence, shotcode, "data", "camera", "*.ma")

    def find_camera_files(self):
        shotDict = {}
        for path in glob.iglob(self.pathTemplate):
            rootPath = os.path.dirname(path)
            shotDict.setdefault(rootPath, []).append(path)
        return shotDict

    def get_focal_length(self, cameraPaths):
        for path in reversed(sorted(cameraPaths, key=lambda p: p.replace("_", "."))):
            pattern = r'".focal_length"\s+(-?\d+\.?\d*)'
            try:
                with open(path, 'r') as file:
                    lines = file.readlines()
                for line in lines:
                    match = re.search(pattern, line)
                    if match:
                        return float(match.group(1))
            except IOError:
                print(f"Error opening file: {path}")
        return None

    def set_focal_length(self, node, focal_length):
        node['FL'].setValue(str(focal_length))

    def update_focal_length(self):
        shotDict = self.find_camera_files()
        for pathList in shotDict.values():
            cameraPaths = [p for p in pathList if "_camera" in p]
            if cameraPaths:
                focal_length = self.get_focal_length(cameraPaths)
                if focal_length is not None:
                    self.set_focal_length(nuke.thisNode(), focal_length)

# 调用方式
if __name__ == "__main__":
    compPath = nuke.scriptName()
    manager = CameraFocalLengthManager(compPath)
    manager.update_focal_length()
