all: compile run

compile:
	echo "Nothing to do here."

test:
	nosetests tests

run: array object conditional recursion iteration extension reify variation rpn

array:
	sh bin/test.sh tests/case/array.swl

object:
	sh bin/test.sh tests/case/object.swl

conditional:
	sh bin/test.sh tests/case/conditional.swl

recursion:
	sh bin/test.sh tests/case/recursion.swl

iteration:
	sh bin/test.sh tests/case/iteration.swl

extension:
	sh bin/test.sh tests/case/extension.swl

reify:
	sh bin/test.sh tests/case/reify.swl

variation:
	sh bin/test.sh tests/case/variation.swl

rpn:
	echo "RPN TESTING"
	sh bin/rpn.sh
	echo "stdin test"
	echo "5 5 + 25 - 0 1 - * 5 ^" | bin/swndl rpn_program/rpn.swl
	echo "0 2 -" | bin/swndl rpn_program/rpn.swl


swndl:
	sh bin/run.sh bin/swndl

pretty:
	sh bin/run.sh bin/pretty

environment:
	sh bin/environment

parse:
	sh bin/run.sh bin/recognizer

scan:
	sh bin/run.sh bin/scanner

init:
	virtualenv --python=python3 env
	. env/bin/activate && pip install -r requirements.txt --use-mirrors
