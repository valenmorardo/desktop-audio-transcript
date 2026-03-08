@echo off
chcp 65001 >nul
title Transcripción de clases

:: Comprobar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo No se encontró Python. Instalalo desde https://www.python.org/downloads/
    echo Marcá "Add Python to PATH" al instalar.
    pause
    exit /b 1
)

:: Crear venv si no existe
if not exist "venv\Scripts\activate.bat" (
    echo Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo Fallo al crear el entorno virtual.
        pause
        exit /b 1
    )
)

:: Activar e instalar
call venv\Scripts\activate.bat
echo Instalando o actualizando dependencias...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Fallo al instalar dependencias.
    pause
    exit /b 1
)

:: Opcional: avisar si no está ffmpeg (faster-whisper lo necesita)
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo.
    echo Aviso: ffmpeg no está en el PATH. La transcripción puede fallar.
    echo Instalalo desde https://ffmpeg.org/download.html o con: choco install ffmpeg
    echo.
    pause
)

echo.
echo Iniciando la app...
python app.py
pause
