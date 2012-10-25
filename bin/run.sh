#!/bin/bash
# run.sh
#
# author: Christopher S. Corley

if [ "$1" == "quiet" ]; then
    echo $each 
    $2 $each
else
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
fi
