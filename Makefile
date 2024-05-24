MONERO_SIGNER_DIR=../MoneroSigner
EMULATOR_DIR=/projects/monerosigner/monerosigner-emulator

default: load

load: emulator work
	sudo mount -t overlay overlay -o lowerdir=$(MONERO_SIGNER_DIR)/src,upperdir=$(EMULATOR_DIR)/src,workdir=$(EMULATOR_DIR)/work $(EMULATOR_DIR)/emulator

unload:
	sudo umount $(EMULATOR_DIR)/emulator

emulator:
	mkdir -p emulator

work:
	mkdir -p work

install:
	sudo apt-get install python3-tk
	sudo apt install libzbar0
	pip install --upgrade -r requirements.txt

run:
	cd emulator; python main.py
