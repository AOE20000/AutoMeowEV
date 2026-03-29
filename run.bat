@echo off
chcp 65001 >nul
echo ========================================
echo   MeowParser - 喵语解析器
echo ========================================
echo.
echo 正在启动...
echo.

python meow_parser.py

if errorlevel 1 (
    echo.
    echo 启动失败！请检查：
    echo 1. 是否已安装 Python 3.8+
    echo 2. 是否已安装依赖: pip install -r requirements_pyqt6.txt
    echo 3. 是否以管理员身份运行
    echo.
    pause
)
