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