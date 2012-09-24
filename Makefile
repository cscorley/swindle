all: test


test:
	nosetests tests


init:
	pip install -r requirements.txt --use-mirrors
