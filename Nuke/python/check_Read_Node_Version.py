
#用来检测文件夹下是否有新的版本，如果有就更新路径，如果没有就跳过

import nuke
import os
import re

read_nodes = [node for node in nuke.allNodes() if node.Class() == 'Read']

def extract_version(file_path):
    match = re.search(r'v\d+', file_path)
    if match:
        return match.group()
    else:
        return None
    
for node in read_nodes:

    file_path = node['file'].value()
    
    dir_path = os.path.dirname(file_path)
    
    version = extract_version(dir_path)
    
    check_path = dir_path[:-5]
    
    subfolders = [f for f in os.listdir(check_path) if os.path.join(check_path,f)]
    subfolders.sort()
    
    if version and subfolders:
        highest_version = subfolders[-1]
        if version != highest_version:
            new_file_path = file_path.replace(version, highest_version)
            node['file'].setValue(new_file_path)