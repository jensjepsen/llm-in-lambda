ACTIVATE=$(shell echo "`pwd`/venv/bin/activate")
PYTHON=$(shell echo "`pwd`/venv/bin/python")

venv/touchfile: requirements.dev.txt cdk/requirements.txt model_lambda/requirements.txt
	python3 -m virtualenv venv
	. $(ACTIVATE) && pip install -r requirements.dev.txt
	. $(ACTIVATE) && pip install -r cdk/requirements.txt
	. $(ACTIVATE) && pip install -r model_lambda/requirements.txt
	touch venv/touchfile

cli: venv/touchfile
	. $(ACTIVATE) && $(PYTHON) -m cli $(ARGS)

server: venv/touchfile
	. $(ACTIVATE) && $(PYTHON) -m uvicorn model_lambda.index:app

export DOCKER_BUILDKIT=1
deploy: venv/touchfile
	. $(ACTIVATE) && cd cdk && cdk deploy --require-approval never