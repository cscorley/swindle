all: compile test

compile:

test:
	nosetests tests

run:
	sh bin/run.sh bin/recognizer

init:
	virtualenv env
	pip install -r requirements.txt --use-mirrors
