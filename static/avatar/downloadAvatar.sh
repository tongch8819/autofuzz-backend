#!/bin/bash

for i in {1..50}; do
	curl https://api.prodless.com/avatar.png?size=50 -o $i.png
done
