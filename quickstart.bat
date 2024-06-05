@echo off

set MONERO_SIGNER_DIR=..\MoneroSigner
set EMULATOR_DIR=.
set DIST_DIR=dist
set BUILD_DIR=build

if "%1"=="load" goto load
if "%1"=="unload" goto unload
if "%1"=="install" goto install
if "%1"=="run" goto run
if "%1"=="executable" goto executable
if "%1"=="clean" goto clean

:load
mkdir "%EMULATOR_DIR%\emulator"
xcopy /E /I "%MONERO_SIGNER_DIR%\src" "%EMULATOR_DIR%\emulator"
xcopy /E /I "%EMULATOR_DIR%\src" "%EMULATOR_DIR%\emulator"
goto end

:unload
rmdir /S /Q "%EMULATOR_DIR%\emulator"
goto end

:install
pip install --upgrade -r requirements.txt
goto end

:run
cd "%EMULATOR_DIR%\emulator"
python main.py
goto end

:executable
pip install -U pyinstaller
mkdir "%DIST_DIR%" 2>nul
mkdir "%BUILD_DIR%" 2>nul
rmdir /S /Q "%BUILD_DIR%"
rmdir /S /Q "%DIST_DIR%"
xcopy /E /I "%MONERO_SIGNER_DIR%\src" "%BUILD_DIR%"
xcopy /E /I "%EMULATOR_DIR%\src" "%BUILD_DIR%"
pyinstaller --onefile -n xmrsigner --add-data "%BUILD_DIR%\seedsigner\resources;seedsigner\resources" --collect-all seedsigner --collect-data "seedsigner;seedsigner" --hidden-import PIL._tkinter_finder --collect-submodules PIL --collect-submodules PIL.ImageTk "%BUILD_DIR%\main.py"
goto end

:clean
for /d /r "%EMULATOR_DIR%" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
goto end

:end
