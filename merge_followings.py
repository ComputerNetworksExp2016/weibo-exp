import pickle

data = pickle.load(open('merged.pickle', 'rb'))

for i in range(40):
    for uid, followings in pickle.load(open('followings/followings_{}.pickle'.format(i), 'rb')).items():
        data['users'][uid].following_uids = followings

pickle.dump(data, open('all.pickle', 'wb'))
