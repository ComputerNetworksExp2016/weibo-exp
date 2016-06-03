from pathlib import Path
import pickle
from weibo.weibo import Weibo

DATA_FILE = 'data.pickle'
TOPIC = '1008086d2d90115bda1a5fdcba46100f379dd9'

if Path(DATA_FILE).exists():
    data = pickle.load(open(DATA_FILE, 'rb'))
    # print(len(data['topic_posts']))
else:
    exit()

def get_count(key):

	count = {
		'location': {},
		'age': {},
		'gender': {}
	}

	for i in data[key]:

		user = data[key][i]
		if user is None:
			continue

		l = user.location
		a = user.age
		g = user.gender
		
		if l is None:
			l = '-1'
		else:
			l = l.split()[0] # classify location by province

		if a is None:
			a = -1
		else:
			a = int(a)

		if g is None:
			g = '-1'

		location_num = (count['location']).get(l)
		age_num = count['age'].get(a)
		gender_num = count['gender'].get(g)

		if location_num is None:
			count['location'][l] = 1
		else:
			count['location'][l] += 1

		if age_num is None:
			count['age'][a] = 1
		else:
			count['age'][a] += 1

		if gender_num is None:
			count['gender'][g] = 1
		else:
			count['gender'][g] += 1

	return count

followers_count = get_count('topic_followers')
participants_count = get_count('topic_participants')

# print('topic_followers = ', followers_count)
# print('topic_participants = ', participants_count)

with open('participants.csv', 'w') as file:
	for f in participants_count:
		for info in participants_count[f]:
			file.write('%s,%d\n' % (info, participants_count[f][info]))

with open('followers.csv', 'w') as file:
	for f in followers_count:
		for info in followers_count[f]:
			file.write('%s,%d\n' % (info, followers_count[f][info]))



