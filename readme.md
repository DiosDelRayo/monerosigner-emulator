# MoneroSigner Emulator (fork of [SeedSigner Emulator](https://github.com/enteropositivo/seedsigner-emulator)
> Allows to execute [MoneroSigner](https://github.com/DiosDelRayo/MoneroSigner) air-gapped hardware wallet in your desktop (windows/linux/mac)

![Emulator window](img/screen.png)


## Todo
See the separate [Todo list](Todo.md)

## How it works
A new display driver that replaces the existing _SeedSigner ST7789 1.3_ driver, making possible to execute the device in a desktop enviroment.

>Use it with the integrated buttons or with your keyboard ( Arrow Keys, Enter, 1,2,3 )

The Emulator should still work with [SeedSigner](https://github.com/SeedSigner/seedsigner), but is only tested with [MoneroSigner](https://github.com/DiosDelRayo/MoneroSigner).

To run the **MoneroSigner Emulator** on Linux you need to clone [MoneroSigner](https://github.com/DiosDelRayo/MoneroSigner) and [MoneroSigner Emulator](https://github.com/DiosDelRayo/monerosigner-emulator) in the same folder, then create a virtual environment with `python3 -m venv .`, `make install`, `make load` and `make run` and you are running on Linux the the emulator. On Windows or MacOS I'm not yet aware if there is a an overlay file system (`mount -t overlay`) which is used to run the emulator without to touch anything on any repository.

If you have more then one camera on the system there will appear a dropdown list on the upper left corner to select the camera which will be used next time.

Planed features:
- [x] Build executable for linux on linux
- [x] Build executable for win32 on Windows
- [x] ~~Build AppImage for MacOS on MacOS~~ For MacOS try docker

## Quickstart (Linux, win32, MacOS coming soon)

### Linux
Do following in your console:
```
mkdir -p monerosigner
cd monerosigner
git clone https://github.com/DiosDelRayo/MoneroSigner.git
git clone https://github.com/DiosDelRayo/monerosigner-emulator
cd monerosigner-emulator
python3 -m venv .
source bin/activate
make install
make load
make run
make unload
deactivate
```

For all future uses you can use it simply with:
```
cd monerosigner-emulator
source bin/activate
make load && make run; make unload
```

### Windows
Run the following script to install dependencies:
```
powershell -Command "& {Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/DiosDelRayo/monerosigner-emulator/master/dependencies.ps1?v=' + (Get-Date -Format 'yyyyMMddHHmmss')))}"
```

You need to install also [vcredist](https://www.microsoft.com/en-US/download/details.aspx?id=40784) for your machine.

Then you can build the executable with:
```
.\quickstart.bat executable
```

or run simply the emulator with:
```
.\quickstart.bat load
```
to copy all in on file and then finally:
```
.\quickstart.bat run
```

### MacOS
I thought already Windows is the hell (and it was), but MacOS...
Well, seems that Python TCL/TK is utterly broken. Had years ago that issue, and switched to PyQt because of that. I can't get it work in the VM. With docker it should work, but I can't test. How I have no more Apple machines - end I don't plan ever in my life to get any Apple device. You are on your own except sombody else will test it and gives feedback.

So you can try:
```
docker pull vthor/monerosigner-emulator
VIDEO_DEVICE=/dev/video0
docker run -e DISPLAY=:0 --device=${VIDEO_DEVICE} vthor/monerosigner-emulator
```

## Executables, as soon I have a build chain I will frequently release them in Releases

## Thank you

 Thank you for your work [@EnteroPositivo](https://twitter.com/enteropositivo)on X.
