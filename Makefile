ACTIVATE=$(shell echo "`pwd`/venv/bin/activate")
PYTHON=$(shell echo "`pwd`/venv/bin/python")

venv/touchfile: requirements.txt requirements.dev.txt
	python3 -m virtualenv venv
	. $(ACTIVATE) && pip install -r requirements.txt
	. $(ACTIVATE) && pip install -r requirements.dev.txt
	touch venv/touchfile

cli: venv/touchfile
	. $(ACTIVATE) && $(PYTHON) -m cli $(ARGS)