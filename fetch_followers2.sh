#!/bin/bash
i=151
for username in 17759968584 17759973124 17744035979
do
	python3 fetch_followers2.py $username a123456 $i
	i=$(($i+50))
done
