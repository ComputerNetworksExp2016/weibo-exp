from pathlib import Path
import pickle
from weibo.weibo import Weibo

DATA_FILE = 'data.pickle'
# TOPIC = '100808cd96538eeddd4fe8f836ebcc74674201'

if Path(DATA_FILE).exists():
    data = pickle.load(open(DATA_FILE, 'rb'))
    for l in data:
    	print(l)
    print(data['topic_posts'][3983031792070626])
else:
    exit()

count = {
	'repost_num': {'0-50': 0, '50-100': 0, '100-150': 0, '150-200': 0, '200-300': 0, '300-400': 0, '400-500': 0, '>=500': 0},
	'comment_num': {'0-50': 0, '50-100': 0, '100-150': 0, '150-200': 0, '200-300': 0, '300-400': 0, '400-500': 0, '>=500': 0},
	'like_num': {'0-50': 0, '50-100': 0, '100-150': 0, '150-200': 0, '200-300': 0, '300-400': 0, '400-500': 0, '>=500': 0},
	'time': {}
}

for i in data['topic_posts']:

	post = data['topic_posts'][i]
	if post is None:
		continue

	rn = post.repost_num
	cn = post.comment_num
	ln = post.like_num
	t  = str(post.created_at)

	if 0 <= rn < 50:
		count['repost_num']['0-50'] += 1
	elif 50 <= rn < 100:
		count['repost_num']['50-100'] += 1
	elif 100 <= rn < 150:
		count['repost_num']['100-150'] += 1
	elif 150 <= rn < 200:
		count['repost_num']['150-200'] += 1
	elif 200 <= rn < 300:
		count['repost_num']['200-300'] += 1
	elif 300 <= rn < 400:
		count['repost_num']['300-400'] += 1
	elif 400 <= rn < 500:
		count['repost_num']['400-500'] += 1
	else:
		count['repost_num']['>=500'] += 1

	if 0 <= cn < 50:
		count['comment_num']['0-50'] += 1
	elif 50 <= cn < 100:
		count['comment_num']['50-100'] += 1
	elif 100 <= cn < 150:
		count['comment_num']['100-150'] += 1
	elif 150 <= cn < 200:
		count['comment_num']['150-200'] += 1
	elif 200 <= cn < 300:
		count['comment_num']['200-300'] += 1
	elif 300 <= cn < 400:
		count['comment_num']['300-400'] += 1
	elif 400 <= cn < 500:
		count['comment_num']['400-500'] += 1
	else:
		count['comment_num']['>=500'] += 1

	if 0 <= ln < 50:
		count['like_num']['0-50'] += 1
	elif 50 <= ln < 100:
		count['like_num']['50-100'] += 1
	elif 100 <= ln < 150:
		count['like_num']['100-150'] += 1
	elif 150 <= ln < 200:
		count['like_num']['150-200'] += 1
	elif 200 <= ln < 300:
		count['like_num']['200-300'] += 1
	elif 300 <= ln < 400:
		count['like_num']['300-400'] += 1
	elif 400 <= ln < 500:
		count['like_num']['400-500'] += 1
	else:
		count['like_num']['>=500'] += 1

	t = t.split(' ')[1]
	hour = t.split(':')[0]
	t_num = count['time'].get(hour)
	if t_num is None:
		count['time'][hour] = 1
	else:
		count['time'][hour] += 1


with open('posts.csv', 'w') as file:
	for f in count:
		file.write('%s\n' % f)
		for info in count[f]:
			file.write('%s,%d\n' % (info, count[f][info]))
		file.write('\n')

 




