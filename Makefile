all: compile test

compile:

test:
	nosetests tests

run: test
	sh bin/run.sh

init:
	pip install -r requirements.txt --use-mirrors
