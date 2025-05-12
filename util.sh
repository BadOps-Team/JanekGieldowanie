#!/bin/bash

if [ "$1" == "clean" ]; then
	rm -f graphs/*
elif [ "$1" == "generate" ]; then
	for ((i=1; i < $2; i++)); do
		cp configs/config0.json configs/config${i}.json
	done
fi