#!/bin/bash
i=301
for username in 17759674310 17759675467 17720720836 17759675395
do
	python3 fetch_followers3.py $username a123456 $i
	i=$(($i+50))
done
