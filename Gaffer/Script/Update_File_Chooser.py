import pathlib
import re
import IECore
import Gaffer


def replace_frame_number_with_placeholder(file_path: pathlib.Path) -> pathlib.Path:
    """
    替换文件名中的帧编号为 '####'。
    假设帧编号是文件名中的一串连续数字，且通常出现在文件名的末尾或中间部分。
    """
    stem = file_path.stem
    match = re.search(r"(\d+)(?=\D*$)", stem)  
    if match:
        new_stem = re.sub(r"(\d+)(?=\D*$)", "####", stem)
        return file_path.with_stem(new_stem)
    else:
        return file_path

def process_file_paths(file_paths: list[pathlib.Path]) -> tuple[IECore.StringVectorData, IECore.StringVectorData]:
    """
    处理文件路径列表，将文件名中的帧编号替换为 '####'，并去重。
    返回处理后的文件路径和文件名。
    """
    new_file_paths = {replace_frame_number_with_placeholder(f): None for f in file_paths}.keys()
    new_file_names = {f.stem for f in new_file_paths}
    return IECore.StringVectorData([str(f) for f in new_file_paths]), IECore.StringVectorData(list(new_file_names))

node = plug.node()
directory = node["directory"].getValue()

directory = pathlib.Path(directory).as_posix()

files = list(pathlib.Path(directory).glob("*.exr"))

file_paths, file_names = process_file_paths(files)

node["filesFound"].setValue(file_paths)
print(file_paths,file_names)

Gaffer.Metadata.registerValue(node["fileChooser"], "presetNames", file_names)
Gaffer.Metadata.registerValue(node["fileChooser"], "presetValues", file_paths)