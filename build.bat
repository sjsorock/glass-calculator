@echo off
chcp 65001
echo 正在安装依赖...
python -m pip install pyinstaller
echo.
echo 正在打包计算器...
pyinstaller --onefile --windowed --name Calculator glass_calculator.py
echo.
echo 打包完成！
echo 可执行文件位于: dist\Calculator.exe
pause
