all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

gen-proto:
	protoc --python_out='.' ./graph_curation/protos/*.proto

interactive:
	venv/bin/pip install bpython ipython pylint pep8 flake8 pydocstyle rope

venv:
	virtualenv --python=python3 venv && venv/bin/python setup.py develop

venv-interactive: venv interactive

run: venv
	FLASK_APP=graph_curation_flask GRAPH_CURATION_SETTINGS=../settings.cfg venv/bin/flask run --host "0.0.0.0" --port=5000

test: venv
	GRAPH_CURATION_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist
