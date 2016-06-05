#!/bin/bash
i=151
for username in 17720720793 17720720787 17720821134
do
	python3 fetch_followers.py $username a123456 $i
	i=$(($i+50))
done