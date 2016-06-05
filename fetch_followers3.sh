#!/bin/bash
i=301
for username in 18120852841 17053797946 18117515441 15396097845
do
	python3 fetch_followers3.py $username a123456 $i
	i=$(($i+50))
done
