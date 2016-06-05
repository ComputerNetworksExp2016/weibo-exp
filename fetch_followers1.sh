#!/bin/bash
i=1
for username in 17759974744 17759967742 17759968467
do
	python3 fetch_followers1.py $username a123456 $i
	i=$(($i+50))
done
