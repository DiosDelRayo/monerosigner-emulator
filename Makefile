MONERO_SIGNER_DIR=../MoneroSigner
EMULATOR_DIR=.
DIST_DIR=dist
BUILD_DIR=build

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

executable:
	pip install -U pyinstaller
	mkdir -p ${DIST_DIR}
	mkdir -p ${BUILD_DIR}
	rm -rf ${BUILD_DIR}/*
	rm -rf ${DIST_DIR}/*
	cp -ar ${MONERO_SIGNER_DIR}/src/* build/
	cp -ar ${EMULATOR_DIR}/src/* build/
	pyinstaller --onefile -n xmrsigner --add-data "${BUILD_DIR}/seedsigner/resources:seedsigner/resources" --collect-all seedsigner --collect-data "seedsigner:seedsigner" --hidden-import PIL._tkinter_finder --collect-submodules PIL --collect-submodules PIL.ImageTk ${BUILD_DIR}/main.py

clean:
	find src -type d -name __pycache__ -exec rm -rf \{\} \;
	find emulator -type d -name __pycache__ -exec rm -rf \{\} \;
