include mk/python.mk
DCURL_DIR := deps/dcurl
DCURL_LIB := $(DCURL_DIR)/build/libdcurl.so
DEPS += $(DCURL_LIB)

all: $(DEPS)

.PHONY: $(DCURL_LIB)
$(DCURL_LIB): $(DCURL_DIR)
	git submodule update --init $^
	git submodule update --remote $^
	$(MAKE) -C $^ config
	@echo
	$(info Modify $^/build/local.mk for your environments.)
	$(MAKE) -C $^ all

TESTS += $(wildcard tests/*.py)
TESTS += $(wildcard tests/tangleid/*.sh)

check: server.py $(DCURL_LIB)
	@ TMP_PID=`mktemp /tmp/server_pid.XXXXXX`; \
	echo "Running test suite..." ; \
	( $(PYTHON) $^ & echo $$! > $${TMP_PID} ); \
	sleep 3 ; \
	for i in $(TESTS); do \
	    ( echo "\n\n==[ $$i ]==\n"; $$i || kill -9 `cat $${TMP_PID}` ) \
	done ; \
	kill -9 `cat $${TMP_PID}`
	@$(RM) $${TMP_PID}

clean:
	find . -name '*.pyc' | xargs $(RM)
	$(MAKE) -C $(DCURL_DIR) clean
distclean: clean
	$(RM) -r $(DCURL_DIR)
	git checkout $(DCURL_DIR)
