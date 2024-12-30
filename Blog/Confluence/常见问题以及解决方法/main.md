# 常见问题以及解决方法

## linux 下安装达芬奇软件

正常下载DaVinci_Resolve_Studio_18.6.6_Linux  按照pdf安装

需注意

最后一步，需在root权限下。找it  su一下

```shell
sudo ./DaVinci_Resolve_Studio_18.6.6_Linux.run -a -i
```

然后装完破解

```shell
sudo perl -pi -e 's/\x00\x85\xc0\x74\x7b\xe8/\x00\x85\xc0\xEB\x7b\xe8/g' /opt/resolve/bin/resolve
sudo perl -pi -e 's/\x00x85\xc0\x74x7b\xe8/\x00x85\xc0\xEBx7b\xe8/g' /opt/resolve/bin/resolve
```

## linux 飞书客户端缓存问题

定时清理对应文件夹下的 .config/LarkShell/sdk_storage/ 即可

```shell
#!/bin/bash

# 指定要清空的文件夹路径
FOLDER="$HOME/.config/LarkShell/sdk_storage"

# 检查文件夹是否存在
if [ -d "$FOLDER" ]; then
    # 删除文件夹内的所有内容
    rm -rf "$FOLDER"/*
    echo "已清空文件夹：$FOLDER"
else
    echo "文件夹不存在：$FOLDER"
fi
```

## nuke Slate需要添加相机的focal_length数值怎么办

```python
import nuke, glob, os, re
 
def get_sequence_shotcode(compPath):
    splits = os.path.basename(compPath).split("_")
    sequence = splits[0]
    shotcode = shotcode = '_'.join(code for code in os.path.basename(compPath).split(".")[0].split("_")[1:-2])
    return sequence, shotcode
 
def create_path_template(sequence, shotcode):
    return os.path.join("$proj", "pj2024cg016", "sequences", sequence, shotcode, "data", "camera", "*.ma")
 
def find_camera_files(path_template):
    shotDict = {}
    for path in glob.iglob(path_template):
        rootPath = os.path.dirname(path)
        shotDict.setdefault(rootPath, []).append(path)
    return shotDict
 
def get_focal_length(cameraPaths):
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
 
def set_focal_length(node, focal_length):
    # 将浮点数转换为字符串
    node['FL'].setValue(str(focal_length))
 
def main():
    compPath = nuke.scriptName()
    sequence, shotcode = get_sequence_shotcode(compPath)
    pathTemplate = create_path_template(sequence, shotcode)
    pathTemplate = os.path.expandvars(pathTemplate)
    shotDict = find_camera_files(pathTemplate)
 
    for pathList in shotDict.values():
        cameraPaths = [p for p in pathList if "_camera" in p]
        if cameraPaths:
            focal_length = get_focal_length(cameraPaths)
            if focal_length is not None:
                set_focal_length(nuke.thisNode(), focal_length)
 
if __name__ == "__main__":
    main()
```

## nuke中自动检测Read节点，并且替换路径为文件夹中的最新版本号

测试环境：目前只在linux上测试可行，适用于灯光更新所有read节点

```python
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
     
    check_path = dir_path.replace(f'/{version}', '')
    #如果是立体视频，这里对路径还需要进行一次清理
    #check_path = check_path.replace('%V', 'left')
    subfolders = [f for f in os.listdir(check_path) if os.path.join(check_path,f)]
    subfolders.sort()
     
    if version and subfolders:
        highest_version = subfolders[-1]
        if version != highest_version:
            new_file_path = file_path.replace(version, highest_version)
            node['file'].setValue(new_file_path)
```

## OpenCue 渲染命令行详解(简单粗糙版)

指定项目和maya版本,调用mtok模块的render函数,-f指定要渲染的文件,-r指定渲染图片输出的路径,-l指定渲染层,-c指定渲染相机-s,-e,-b没啥说的,开始结束

```shell
rez-env pj2023cg028 maya==2022
--
mayapy -m mtok render
-f I:/proj/pj2023cg028/sequences/s012/s012_0010/lighting/publish/maya/s012_0010_lit.v009.ma
-r I:/proj/pj2023cg028/syncData/render/s012/s012_0010/images/full
-l Matte -c S012_0010_:S012_0010_rlo:rig_camera_shakeShape
-s 1001
-e 1001
-b 1
```

这里还是通过maya批处理命令导出成规范的ass,例如这里导出的是 mtok_export/Matte/1001.ass

```shell
launch subprocess cmdline: rez-env pj2023cg028 maya==2022
--
mayabatch -command
"python(\"
import mtok;
mtok.export_scene(\\\"I:/proj/pj2023cg028/sequences/s012/s012_0010/lighting/publish/maya/s012_0010_lit.v009.ma\\\", \\\"C:/Users/qubeproxy/Documents/Temp/mtok/16c51fbd/mtok_export\\\", 1001, 1001, 1, \\\"S012_0010_:S012_0010_rlo:rig_camera_shakeShape\\\", \\\"Matte\\\")\")"

```

这里就直接kick调用渲染就完事了

```shell
launch subprocess cmdline: rez-env maya==2022 mtoa==5.1.3
--
kick -dw -dp -nstdin -i C:/Users/qubeproxy/Documents/Temp/mtok/16c51fbd/mtok_export/Matte/1001.ass -l L:/centralizedRepo/third_party/mtoa/win/5.1.3/2022/procedurals -v 4
```

渲染完毕拷贝走

## roughlayout场景探索阶段在Breakdown中导出所有的相机

```python
cameras = list()
 
for camera in cmds.ls("*rig_camera", r=1):
    camera = cmds.rename(camera, camera.rsplit("|", 1)[-1].replace(":", "__"))
    cameras.append(camera)
 
cmds.select(cameras, r=1)
```

## 快速在Daily文件夹中创建当天日期的文件夹

windows

```powershell
@echo off
setlocal
 
REM 获取当前日期
for /f "tokens=2-3 delims=/ " %%a in ('echo %date%') do (
    set "day=%%b"
    set "month=%%a"
)
 
echo %day%
echo %month%
REM 去掉日期中的空格
set "day=%day: =%"
set "month=%month: =%"
 
REM 格式化月份和日期为两位数
if %month% lss 10 set "month=%month%"
if %day% lss 10 set "day=%day%"
 
REM 组合日期为文件夹名
set "folder_name=%month%%day%"
 
REM 判断文件夹是否存在，如果不存在则创建
if not exist "%folder_name%\" (
    mkdir "%folder_name%"
    echo Folder %folder_name% created successfully.
) else (
    echo Folder %folder_name% already exists, no need to create.
)
 
pause
```

linux

```shell
#!/bin/bash
 
# 获取当前日期
day=$(date +"%d")
month=$(date +"%m")
 
echo $day
echo $month
 
# 去掉日期中的空格
day=$(echo $day | tr -d ' ')
month=$(echo $month | tr -d ' ')
 
# 格式化月份和日期为两位数
if [ $month -lt 10 ]; then
    month="$month"
fi
 
if [ $day -lt 10 ]; then
    day="$day"
fi
 
# 组合日期为文件夹名
folder_name="${month}${day}"
 
# 判断文件夹是否存在，如果不存在则创建
if [ ! -d "$folder_name" ]; then
    mkdir "$folder_name"
    echo "Folder $folder_name created successfully."
else
    echo "Folder $folder_name already exists, no need to create."
fi
```

## 批量为选择的灯光连接一个相同的lightFilters

```python
import maya.cmds as cmds
 
selected_lights = cmds.ls(selection=True)
light_filter = cmds.createNode('aiLightDecay')
 
for light in selected_lights:
    cmds.connectAttr(light_filter + '.message', light + '.aiFilters[0]', force=True)
```

## 文件夹操作

在前环节修型修完之后，升级了版本补渲了修型的几帧。

出现了一个问题记录一下

正常最终版本‘v06’
修型版本‘v07’（但是可能只有1，2，5，7这几帧）

合成拿到之后不好操作，需要灯光给一个完整的序列版本。

解决方案：

这个项目上的操作是新建一个‘v08’，把‘v06’拷贝进来，然后再把‘v07’拷贝进来做覆盖即可。提供一个py脚本，抛砖引玉一下

```python
import os
import shutil
 
folder_path = '这里填到images/full/cha_10为止即可'
new_version = '想要新建的版本号例如v026'
 
subfolders = [f for f in os.listdir(folder_path) if os.path.join(folder_path,f)]
subfolders.sort()
 
new_folder_path = os.path.join(folder_path,new_version)
 
os.makedirs(new_folder_path)
 
for subfolder in subfolders[-2:]:
    subfolder_path = os.path.join(folder_path,subfolder)
    files = os.listdir(subfolder_path)
    for file in files:
        file_path = os.path.join(subfolder_path,file)
        shutil.copy(file_path,new_folder_path)
         
print('Success')
```

## 立体相机左右眼导出相机给外包

```python
from cameraUtils import cameraBakeTool
 
baker = cameraBakeTool.CameraBakeTool()
 
baker.bakeCamera(filePath = "/mnt/proj_M/pj2024cg002/syncData/workgroup/Lgt_Workgroup/Daily/0619/sc02_10_left.ma", newCameraName = None, bakeMode = "shake", frameRange = baker.getFrameRange(inner = True),
        keepImagePlane = False, timewarpStatus = None, unwarpFrameRange = True, recoverTimecode = False, timecodeFps = None,
        specifiedCamera = 'stereoCameraRight', autoMotionRange = baker.getFrameRange(inner = False), )
```

## 选择多个模型，在对应模型位置生成一盏灯光

```python
import maya.cmds as cmds
 
selected_objects = cmds.ls(selection=True)
 
for obj in selected_objects:
 
    obj_center = cmds.objectCenter(obj, gl=True)
     
    area_light = cmds.shadingNode('aiAreaLight', asLight=True)
     
    cmds.move(obj_center[0], obj_center[1], obj_center[2], area_light)
```

## 项目前期经常需要abc导出导入，快速加载abc插件

```python
import maya.cmds as cmds
cmds.loadPlugin('AbcImport.mll')
```

## 项目文件数量对比

```python
import os
 
def count_files_in_folder(folder_path):
    total_files = 0
     
    # 遍历文件夹内所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)
     
    return total_files
 
# 获取指定路径下的文件夹名称
def get_subfolder_names(parent_folder):
    subfolders = [f.path for f in os.scandir(parent_folder) if f.is_dir()]
    return subfolders
 
# 指定路径
parent_folder = 'M:/proj_M/pj2023cg021/syncData/workgroup/Comp_WorkGrp/collect'
 
# 获取文件夹名称
subfolders = get_subfolder_names(parent_folder)
 
# 遍历每个文件夹并计算文件数量
for folder in subfolders:
    folder_name = os.path.basename(folder)
    file_count = count_files_in_folder(folder)
    print(f"文件夹 '{folder_name}' 内共有 {file_count} 个文件。")
```

