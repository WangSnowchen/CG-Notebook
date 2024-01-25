#在前环节修型修完之后，升级了版本补渲了修型的几帧。

#出现了一个问题记录一下
#
#正常最终版本‘v06’
#修型版本‘v07’（但是可能只有1，2，5，7这几帧）
#
#合成拿到之后不好操作，需要灯光给一个完整的序列版本。
#
#解决方案：
#
#这个项目上的操作是新建一个‘v08’，把‘v06’拷贝进来，然后再把‘v07’拷贝进来做覆盖即可。提供一个py脚本，抛砖引玉一下



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