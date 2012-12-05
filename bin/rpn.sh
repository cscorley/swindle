#!/bin/bash
# run.sh
#
# author: Christopher S. Corley

for each in `ls rpn/*.txt`; do
    echo ""
    echo "--------------------"
    echo $each " contents:"
    echo "--------------------"
    cat $each
    echo "--------------------"
    echo "RPN results:"
    echo "--------------------"
    bin/swndl rpn/rpn.swl $each
done
