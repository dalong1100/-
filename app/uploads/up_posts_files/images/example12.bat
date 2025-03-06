@echo off
setlocal enabledelayedexpansion

:: 设置目标目录，默认为当前目录
set "dir=."

:: 初始化文件计数
set count=1

:: 遍历目录中的所有文件
for %%f in (%dir%\*) do (
    :: 如果是文件而非目录
    if not "%%~xf"=="" (
        :: 格式化数字，确保双位数
        set num=0!count!
        set num=!num:~-2!

        :: 重命名文件
        ren "%%f" "example!num!.png"

        :: 计数递增
        set /a count+=1
    )
)

echo 重命名完成
pause
