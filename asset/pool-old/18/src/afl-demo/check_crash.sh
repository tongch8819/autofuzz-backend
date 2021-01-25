#!/bin/bash

if [ $# -lt 1 -o $# -gt 2 ]; then
    echo "Usage: $0 <WD> <LogD>"
    exit 1
fi

workDir=$1
logDir=$2
if [ "$2" = "" ]; then
    logDir="."
fi
logName="info.txt"
logPath=${logDir}/${logName}
if [ -e $logPath ]; then
    rm $logPath
fi
touch $logPath

for file in ${workDir}/*; do
    tmp=$(basename $file)
    if [ ! ${tmp%%:*} = "id" ]; then
        continue
    fi
    #echo $file
    echo "Name:" $file >> $logPath
    xxd $file >> $logPath
    echo "" >> $logPath
done
