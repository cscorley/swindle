#!/bin/bash
# run.sh
#
# author: Christopher S. Corley

for each in `ls tests/case/*`; do
    echo ""
    echo ""
    echo "********************"
    echo "--------------------"
    echo $each " contents:"
    echo "--------------------"
    cat $each
    echo "--------------------"
    echo "$1 results:"
    echo "--------------------"
    $1 $each
done

for each in `ls swindle/library/*`; do
    echo ""
    echo ""
    echo "********************"
    echo "--------------------"
    echo $each " contents:"
    echo "--------------------"
    cat $each
    echo "--------------------"
    echo "$1 results:"
    echo "--------------------"
    $1 $each
done
