all: compile test

compile:
	echo "Nothing to do here."

test:
	nosetests tests

run: parse

environment:
	sh bin/environment

parse:
	sh bin/run.sh bin/recognizer

scan:
	sh bin/run.sh bin/scanner

init:
	virtualenv env
	pip install -r requirements.txt --use-mirrors
