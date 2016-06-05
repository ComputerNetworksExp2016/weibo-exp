#!/bin/bash
i=1
for username in 17720822534 17720720796 17720720763
do
	python3 fetch_followers1.py $username a123456 $i
	i=$(($i+50))
done
