#!/bin/bash
# test.sh
#
# author: Christopher S. Corley

echo "=============="
echo "File contents:"
echo "${1}"
echo "=============="

cat ${1}

echo "=============="
echo "Making pretty:"
echo "${1}"
echo "=============="

bin/pretty ${1}

echo "=============="
echo "Executing file:"
echo "${1}"
echo "=============="

bin/swndl ${1}
