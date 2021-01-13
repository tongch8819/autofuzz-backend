#!/bin/bash

# this must be a full path
BASE_DIR=$1
if test $# != 1 || test ! -d $BASE_DIR; then
    echo "Invalid base directory!!!"
    exit 1
fi
DIRS=('bin' 'src' 'input' 'output')
for name in ${DIRS[*]}; do
    mkdir $BASE_DIR/$name
done
# echo "Init finished"