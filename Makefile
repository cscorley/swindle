all: compile 

compile:

test:
	nosetests tests

run:
	sh bin/run.sh

init:
	pip install -r requirements.txt --use-mirrors
