import re
import json

ass_file_path = 'D:/Gaffer_Dev/temp/lighttest_02.ass'

# 打开ASS文件，并读取其中的内容
with open(ass_file_path, 'r') as file:
    content = file.read()

pattern = r'(\w+_light)\s*{([^}]*)}'
matches = re.finditer(pattern, content, re.DOTALL)

for match in matches:
    light_type = match.group(1)
    data_str = match.group(2)
    data_dict = dict(re.findall(r'(\w+)\s+([^\n]+)', data_str))
    
    # 将每个灯光的数据存储为单独的JSON文件
    with open(f'D:/Gaffer_Dev/temp/{light_type}_data.json', 'w') as file:
        json.dump({light_type: data_dict}, file, indent=4)
