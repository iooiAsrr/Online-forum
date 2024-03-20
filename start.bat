@echo off
echo Installing Flask...
pip install flask

echo.
echo Installing Flask-MySQLdb...
pip install flask_mysqldb

echo.
echo Running app.py...
start python app.py

echo.
echo Opening browser at http://127.0.0.1:5000...
start http://127.0.0.1:5000


rem 关闭当前窗口
taskkill /f /im cmd.exe