from pathlib import Path
import pickle
from weibo.weibo import Weibo

DATA_FILE = 'data.pickle'
TOPIC = '1008086d2d90115bda1a5fdcba46100f379dd9'

if Path(DATA_FILE).exists():
    data = pickle.load(open(DATA_FILE, 'rb'))
else:
    exit()

def get_count(key):

	count = {
		'location': {},
		'age': {},
		'gender': {}
	}

	for i in data[key]:

		l = data[key][i].location
		a = data[key][i].age
		g = data[key][i].gender

		location_num = count['location'].get(location)
		age_num = count['age'].get(age)
		gender_num = count['gender'].get(gender)

		if location_num is None:
			count['location'][location] = 1
		else:
			count['location'][location] += 1

		if age_num is None:
			count['age'][age] = 1
		else:
			count['age'][age] += 1

		if gender_num is None:
			count['gender'][gender] = 1
		else:
			count['gender'][gender] += 1
	return count

followers_count = get_count('topic_followers')
participants_count = get_count('topic_participants')






