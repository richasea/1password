SCRIPTS=$(wildcard bin/*)

all: pylint

.PHONY: pylint

pylint: $(SCRIPTS)
	pylint --rcfile=dev/pylint.rc $(SCRIPTS)
