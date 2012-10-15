all: compile 

compile:

test:
	nosetests tests

run:
	sh bin/run.sh

init:
	pip install -r requirements.txt --use-mirrors

prep:
	rm -rf /tmp/submit;
	cp -R ./ /tmp/submit;
	rm -rf /tmp/submit/env;
