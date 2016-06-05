from pathlib import Path
import pickle
from weibo.weibo import Weibo

DATA_FILE = 'data3.pickle'
TOPIC = '100808cd96538eeddd4fe8f836ebcc74674201'

if Path(DATA_FILE).exists():
    data = pickle.load(open(DATA_FILE, 'rb'))
else:
    data = {
        'topic_posts': {},
        'topic_participants': {},
        'topic_followers': {},
        'users': {}
    }

client = Weibo.from_pickle()
# client.save()

def get_user(uid):
    user = data['users'].get(uid)
    if user is None:
        user = client.user(uid)
        data['users'][uid] = user
    return user

# for post in client.topic_posts(TOPIC):
#     data['topic_posts'][post.mid] = post
#     data['topic_participants'][post.uid] = get_user(post.uid)

#     client.save()
#     pickle.dump(data, open(DATA_FILE, 'wb'))

for uid in client.topic_followers(TOPIC):
    data['topic_followers'][uid] = get_user(uid)

    # client.save()
    pickle.dump(data, open(DATA_FILE, 'wb'))
