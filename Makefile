all: compile test

compile:

test:
	nosetests tests

run: parse 

parse:
	sh bin/run.sh bin/recognizer

scan:
	sh bin/run.sh bin/scanner

init:
	virtualenv env
	pip install -r requirements.txt --use-mirrors
