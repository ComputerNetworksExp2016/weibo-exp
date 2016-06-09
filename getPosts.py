from pathlib import Path
import pickle
from weibo.weibo import Weibo

DATA_FILE = 'data.pickle'
# TOPIC = '100808cd96538eeddd4fe8f836ebcc74674201'

if Path(DATA_FILE).exists():
    data = pickle.load(open(DATA_FILE, 'rb'))
else:
    exit()

count = {
	'repost_num': {'0': 0, '1~5': 0, '5~10': 0, '10~15': 0, '15~20': 0, '20~50': 0, '50~100': 0, '>=100': 0},
	'comment_num': {'0': 0, '1~5': 0, '5~10': 0, '10~15': 0, '15~20': 0, '20~50': 0, '50~100': 0, '>=100': 0},
	'like_num': {'0': 0, '1~5': 0, '5~10': 0, '10~15': 0, '15~20': 0, '20~50': 0, '50~100': 0, '>=100': 0},
	'day': {},
	'hour': {}
}

for i in data['topic_posts']:

	post = data['topic_posts'][i]
	if post is None:
		continue

	rn = post.repost_num
	cn = post.comment_num
	ln = post.like_num
	t  = str(post.created_at)

	if rn == 0:
		count['repost_num']['0'] += 1
	elif 1 <= rn < 5:
		count['repost_num']['1~5'] += 1
	elif 5 <= rn < 10:
		count['repost_num']['5~10'] += 1
	elif 10 <= rn < 15:
		count['repost_num']['10~15'] += 1
	elif 15 <= rn < 20:
		count['repost_num']['15~20'] += 1
	elif 20 <= rn < 50:
		count['repost_num']['20~50'] += 1
	elif 50 <= rn < 100:
		count['repost_num']['50~100'] += 1
	else:
		count['repost_num']['>=100'] += 1

	if cn == 0:
		count['comment_num']['0'] += 1
	elif 1 <= cn < 5:
		count['comment_num']['1~5'] += 1
	elif 5 <= cn < 10:
		count['comment_num']['5~10'] += 1
	elif 10 <= cn < 15:
		count['comment_num']['10~15'] += 1
	elif 15 <= cn < 20:
		count['comment_num']['15~20'] += 1
	elif 20 <= cn < 50:
		count['comment_num']['20~50'] += 1
	elif 50 <= cn < 100:
		count['comment_num']['50~100'] += 1
	else:
		count['comment_num']['>=100'] += 1

	if ln == 0:
		count['like_num']['0'] += 1
	elif 0 <= ln < 5:
		count['like_num']['1~5'] += 1
	elif 5 <= ln < 10:
		count['like_num']['5~10'] += 1
	elif 10 <= ln < 15:
		count['like_num']['10~15'] += 1
	elif 15 <= ln < 20:
		count['like_num']['15~20'] += 1
	elif 20 <= ln < 50:
		count['like_num']['20~50'] += 1
	elif 50 <= ln < 100:
		count['like_num']['50~100'] += 1
	else:
		count['like_num']['>=100'] += 1

	day = t.split(' ')[0]
	hour = t.split(' ')[1]
	hour = hour.split(':')[0]

	hour_num = count['hour'].get(hour)
	if hour_num is None:
		count['hour'][hour] = 1
	else:
		count['hour'][hour] += 1
	day_num = count['day'].get(day)
	if day_num is None:
		count['day'][day] = 1
	else:
		count['day'][day] += 1

with open('posts.csv', 'w') as file:
	for f in count:
		file.write('%s\n' % f)
		for info in sorted(count[f]):
			file.write('%s,%d\n' % (info, count[f][info]))
		file.write('\n')

 




