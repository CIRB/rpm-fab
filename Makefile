.PHONY        = install
INSTALL_PATH  = $(abspath env)
BIN_PATH      = $(INSTALL_PATH)/bin

$(BIN_PATH):
	echo $(BIN_PATH)
	virtualenv --python=python2.7 $(INSTALL_PATH) --system-site-packages
	curl https://bootstrap.pypa.io/ez_setup.py | $(BIN_PATH)/python
	curl https://bootstrap.pypa.io/get-pip.py  | $(BIN_PATH)/python

install: $(BIN_PATH)
	$(BIN_PATH)/python setup.py install
