MONERO_SIGNER_DIR=../MoneroSigner
EMULATOR_DIR=.
DIST_DIR=dist
BUILD_DIR=build
VIDEO_DEVICE=/dev/video0
VERSION := $(shell grep VERSION ../MoneroSigner/src/xmrsigner/controller.py | awk -F'"' '{ print $$2 }')

default: load

load: emulator work
	@sudo mount -t overlay overlay -o lowerdir=$(MONERO_SIGNER_DIR)/src,upperdir=$(EMULATOR_DIR)/src,workdir=$(EMULATOR_DIR)/work $(EMULATOR_DIR)/emulator

unload:
	@sudo umount $(EMULATOR_DIR)/emulator

emulator:
	@mkdir -p emulator

work:
	@mkdir -p work

install:
	@sudo apt-get install python3-tk
	@sudo apt install libzbar0
	@pip install --upgrade -r requirements.txt

run: clean
	@cd emulator; python -m xmrsigner

turn:
	@$(MAKE) load && $(MAKE) run ; $(MAKE) unload

executable: clean
	@$(MAKE) -C ${MONERO_SIGNER_DIR} clean
	@pip install -U pyinstaller
	@mkdir -p ${DIST_DIR}
	@mkdir -p ${BUILD_DIR}
	@rm -rf ${BUILD_DIR}/* || true
	# @rm -rf ${DIST_DIR}/* || true  # TODO: WTF?
	@cp -ar ${MONERO_SIGNER_DIR}/src/* build/
	@cp -ar ${EMULATOR_DIR}/src/* build/
	@pyinstaller \
		--onefile\
		-n xmrsigner-${VERSION}\
		--add-data "${BUILD_DIR}/xmrsigner/resources:xmrsigner/resources"\
		--add-binary "${BUILD_DIR}/../monero-wallet-rpc:."\
		--collect-all xmrsigner\
		--collect-data "xmrsigner:xmrsigner"\
		--hidden-import PIL._tkinter_finder\
		--collect-submodules PIL\
		--collect-submodules PIL.ImageTk\
		-p ${BUILD_DIR} ${BUILD_DIR}/xmrsigner/__main__.py

clean:
	@find src -type d -name __pycache__ -exec rm -rf \{\} \; || true
	@find emulator -type d -name __pycache__ -exec rm -rf \{\} \; || true
	@rm -rf MoneroSigner || true
	@rm -rf xmrsigner*.spec || true

docker-image:
	@mkdir -p MoneroSigner
	@cp -ar ../MoneroSigner/src MoneroSigner/
	@docker build -t vthor/monerosigner-emulator:${VERSION} .
	@rm -rf MoneroSigner

docker-run: docker-image
	@xhost +local:root
	@docker run -e DISPLAY=:0 --device=${VIDEO_DEVICE}  -v /tmp/.X11-unix:/tmp/.X11-unix vthor/monerosigner-emulator:${VERSION}

docker-push: docker-image
	@docker push vthor/monerosigner-emulator:${VERSION}

update-version:
	@sed -i -e "s/EMULATOR_VERSION = '[0-9]*\.[0-9]*\.[0-9]*'/EMULATOR_VERSION = '${VERSION}'/" src/xmrsigner/emulator/desktopDisplay.py
	@git add src/xmrsigner/emulator/desktopDisplay.py
	@git commit -m 'Updated version to ${VERSION} to match MoneroSigner'

tag-version:
	@git tag -f v${VERSION}

push-tag: update-version tag-version
	@git push --tags -f origin master
