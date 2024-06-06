# quickstart.ps1

$MONERO_SIGNER_DIR = "..\MoneroSigner"
$EMULATOR_DIR = "."
$DIST_DIR = "dist"
$BUILD_DIR = "build"

param (
    [string]$action
)

if ($action -eq "bootstrap") {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

    choco install python -y
    choco install git -y
    choco install vim -y

    mkdir "C:\monerosigner"
    cd "C:\monerosigner"
    git clone https://github.com/DiosDelRayo/MoneroSigner.git
    git clone https://github.com/DiosDelRayo/monerosigner-emulator.git
}
elseif ($action -eq "requirements") {
    pip install --upgrade -r requirements.txt
}
elseif ($action -eq "load") {
    mkdir "$EMULATOR_DIR\emulator"
    xcopy /E /I "$MONERO_SIGNER_DIR\src" "$EMULATOR_DIR\emulator"
    xcopy /E /I "$EMULATOR_DIR\src" "$EMULATOR_DIR\emulator"
}
elseif ($action -eq "unload") {
    rmdir /S /Q "$EMULATOR_DIR\emulator"
}
elseif ($action -eq "install") {
    pip install --upgrade -r requirements.txt
}
elseif ($action -eq "run") {
    cd "$EMULATOR_DIR\emulator"
    python main.py
}
elseif ($action -eq "executable") {
    pip install -U pyinstaller
    mkdir "$DIST_DIR" 2> $null
    mkdir "$BUILD_DIR" 2> $null
    rmdir /S /Q "$BUILD_DIR"
    rmdir /S /Q "$DIST_DIR"
    xcopy /E /I "$MONERO_SIGNER_DIR\src" "$BUILD_DIR"
    xcopy /E /I "$EMULATOR_DIR\src" "$BUILD_DIR"
    pyinstaller --onefile -n xmrsigner --add-data "$BUILD_DIR\seedsigner\resources;seedsigner\resources" --collect-all seedsigner --collect-data "seedsigner;seedsigner" --hidden-import PIL._tkinter_finder --collect-submodules PIL --collect-submodules PIL.ImageTk "$BUILD_DIR\main.py"
}
elseif ($action -eq "clean") {
    Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force
}
elseif ($action -eq "openssh") {
    Write-Host ""
    Write-Host "Please enter your public SSH key that will be used for authentication:"
    $SSH_KEY = Read-Host
    choco install win32-openssh -y --params "/SSHKeyPairProvider:""$SSH_KEY"""
}
