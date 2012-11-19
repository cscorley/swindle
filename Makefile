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
	virtualenv --python=python3 env
	. env/bin/activate && pip install -r requirements.txt --use-mirrors
