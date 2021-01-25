#!/bin/bash

if [ $# != 1 ]; then
	echo "Usage: $0 <num of testcases>"
	exit 1
fi

if [ $1 -lt 1 ]; then 
	echo "Invalid parameter"
	exit 1
fi

i=1
while [ $i -le $1 ]; do
	python generate.py > input/"$i.input"
	let 'i+=1'
done

