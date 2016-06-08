from pathlib import Path
import pickle
from weibo.weibo import Weibo

DATA_FILE = 'followers.pickle'

if Path(DATA_FILE).exists():
    followers = pickle.load(open(DATA_FILE, 'rb'))
    # for l in data:
    # 	print(l)
else:
    exit()

count = {
	'location': {},
	'age': {},
	'gender': {}
}

for i in followers:

	user = followers[i]
	if user is None:
		continue

	l = user.location
	a = user.age
	g = user.gender
	
	if l is None or l == '':
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

with open('followers.csv', 'w') as file:
	for f in count:
		for info in count[f]:
			file.write('%s,%d\n' % (info, count[f][info]))





