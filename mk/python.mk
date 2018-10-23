# check Python version
PY_FAVORED_VER = 3.5
PYTHON := $(shell which "python")
ifndef PYTHON
PYTHON := $(shell which "python3")
endif

ifndef PYTHON
PYTHON := $(shell which "python$(PY_FAVORED_VER)")
endif

ifndef PYTHON
$(error "Python is not executable, try to check the PATH environment variable or \
install python$(PY_FAVORED_VER) package.")
endif # $(shell which "python")

PY_CHECK_VERSION := $(shell $(PYTHON) -V)

ifeq "$(filter $(PY_FAVORED_VER).%, $(PY_CHECK_VERSION))" ""
PYTHON := $(shell which "python"$(PY_FAVORED_VER))
ifdef PYTHON
$(error "Found python$(PY_FAVORED_VER), but it should be set as \
default interpreter, try to set $(PYTHON) in PATH environment variable.")
else
$(error "$(shell python -V):Unsupported python version, only available for Python$(PY_FAVORED_VER).")
endif # PYTHON
endif # "$(filter ...

# check "iota" module in Python installation
PY_CHECK_MOD_IOTA := $(shell python -c "import iota" 2>/dev/null && \
                       echo 1 || echo 0)
ifeq ("$(PY_CHECK_MOD_IOTA)","0")
PIP := $(shell pip -V && echo 1 || echo 0))
PIP_CHECK_VERSION := $(findstring python 3, $(PIP) && echo $@ || echo 0)
endif

ifneq ("$(PIP)", "1")
$(error "PIP package doesn't pre-configured, try to install it.")
endif

ifeq ("$(PIP_CHECK_VERSION)", "0")
PIP_FAVORED_VER = 3
endif

ifeq ("$(PY_CHECK_MOD_IOTA)", "0")
$(error "PyOTA package doesn't pre-configured, install the latest version: pip$(PIP_FAVORED_VER) install pyota")
endif
