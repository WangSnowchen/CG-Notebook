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