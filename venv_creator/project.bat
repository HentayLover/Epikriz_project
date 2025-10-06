@echo off
chcp 65001 >nul

echo ================================
echo    PROJECT TYPE SELECTION
echo ================================
echo.

:menu
echo Select project type:
echo 1 - Regular Python project (work.py)
echo 2 - Jupyter Notebook project (work.ipynb)
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" goto regular_project
if "%choice%"=="2" goto notebook_project

echo Invalid choice! Please try again.
echo.
goto menu

:regular_project
set WORK_FILE=work.py
goto create_project

:notebook_project
set WORK_FILE=work.ipynb
goto create_project

:create_project
echo.
echo Creating %WORK_FILE%...

:: Создаем виртуальное окружение
python -m venv .venv

:: Активируем виртуальное окружение
call .venv\Scripts\activate.bat

:: Обновляем pip
python -m pip install --upgrade pip

:: Устанавливаем зависимости
if "%WORK_FILE%"=="work.ipynb" (
    echo Installing Jupyter...
    pip install jupyter
)

if exist requirements.txt (
    pip install -r requirements.txt
    echo Dependencies installed from requirements.txt
)

:: Создаем рабочий файл
if "%WORK_FILE%"=="work.py" (
    echo print("Hello from Python project!") > work.py
) else (
    echo Creating Jupyter notebook...
    (
        echo {
        echo  "cells": [
        echo    {
        echo      "cell_type": "code",
        echo      "execution_count": null,
        echo      "metadata": {},
        echo      "outputs": [],
        echo      "source": [
        echo        "print('Hello from Jupyter notebook!')"
        echo      ]
        echo    }
        echo  ],
        echo  "metadata": {
        echo    "kernelspec": {
        echo      "display_name": "Python 3", 
        echo      "language": "python",
        echo      "name": "python3"
        echo    }
        echo  },
        echo  "nbformat": 4,
        echo  "nbformat_minor": 4
        echo }
    ) > work.ipynb
)

echo.
echo ================================
echo    PROJECT CREATED!
echo ================================
echo Virtual environment: .venv
echo Work file: %WORK_FILE%
echo.
if "%WORK_FILE%"=="work.ipynb" (
    echo To start Jupyter:
    echo   .venv\Scripts\activate
    echo   jupyter notebook
) else (
    echo To run your project:
    echo   .venv\Scripts\activate  
    echo   python work.py
)
echo.

pause