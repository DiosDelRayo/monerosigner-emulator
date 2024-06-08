$MONERO_SIGNER_DIR = "..\MoneroSigner"
$EMULATOR_DIR = "."
$DIST_DIR = "dist"
$BUILD_DIR = "build"

Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install python -y
choco install git -y

refreshenv

mkdir "C:\monerosigner"
cd "C:\monerosigner"
git clone https://github.com/DiosDelRayo/MoneroSigner.git
git clone https://github.com/DiosDelRayo/monerosigner-emulator.git
