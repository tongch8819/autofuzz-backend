#!/bin/bash


if test -e project.tar.gz; then
	rm project.tar.gz 
fi

if test -d afl-demo; then
	rm -rf afl-demo/
fi

if test "`ls target`" != ""; then
	rm -rf target/*
fi

path="/home/chengtong/auto-fuzz/fuzzing_platform/autofuzz/templates/autofuzz"
if test "`ls $path | grep report`" != ""; then
	rm $path/report*
fi


echo "Clean success"

