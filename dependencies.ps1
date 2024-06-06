$MONERO_SIGNER_DIR = "..\MoneroSigner"
$EMULATOR_DIR = "."
$DIST_DIR = "dist"
$BUILD_DIR = "build"

echo Quickstart

Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install python -y
choco install git -y
choco install vim -y

mkdir "C:\monerosigner"
cd "C:\monerosigner"
'C:\Program Files\Git\bin\git.exe' clone https://github.com/DiosDelRayo/MoneroSigner.git
'C:\Program Files\Git\bin\git.exe' clone https://github.com/DiosDelRayo/monerosigner-emulator.git