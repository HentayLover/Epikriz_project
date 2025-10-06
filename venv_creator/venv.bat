@echo off
echo Creating venv...

:: Создаем виртуальное окружение
python -m venv .venv

:: Активируем виртуальное окружение
call .venv\Scripts\activate.bat

echo Updating pip...
python -m pip install --upgrade pip

echo install library from requirements.txt...

if exist requirements.txt (
    pip install -r requirements.txt
    echo all installed!
) else (
    echo file requirements.txt is not exist!
)

echo.
echo Venv activate!
echo for deactivate write: deactivate
pause