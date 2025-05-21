#!/bin/bash

if [ "$1" == "clean" ]; then
	rm -f graphs/*
	rm -f csv_results/*
elif [ "$1" == "generate" ]; then
	for ((i=1; i <= $2; i++)); do
		cp configs/config${i}_1.json configs/config${i}_4.json
	done
elif [ "$1" == "commit_machine" ]; then
	for ((i=0; i < $2; i++)); do
		if ((i%2 == 0 )); then
			echo "pzdr" > temp
			git add .
			git commit -m "commit$i"
			git push
		else 
			rm -f temp
			git add .
			git commit -m "commit$i"
			git push
		fi
	done
	rm -f temp
fi