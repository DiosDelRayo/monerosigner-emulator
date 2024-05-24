MONERO_SIGNER_DIR=../MoneroSigner
EMULATOR_DIR=/projects/monerosigner/monerosigner-emulator

default: load

load: emulator work
	sudo mount -t overlay overlay -o lowerdir=$(MONERO_SIGNER_DIR)/src,upperdir=$(EMULATOR_DIR)/seedsigner,workdir=$(EMULATOR_DIR)/work $(EMULATOR_DIR)/emulator

unload:
	sudo umount $(EMULATOR_DIR)/emulator

emulator:
	mkdir -p emulator

work:
	mkdir -p work

install:
	sudo apt-get install python3-tk
	sudo apt install libzbar0
	pip install --upgrade Pillow
	pip install --upgrade setuptools
	pip install git+https://github.com/jreesun/urtypes.git@e0d0db277ec2339650343eaf7b220fffb9233241
	pip install git+https://github.com/enteropositivo/pyzbar.git@a52ff0b2e8ff714ba53bbf6461c89d672a304411#egg=pyzbar
	pip install embit dataclasses qrcode tk opencv-python

run:
	cd emulator; python main.py
