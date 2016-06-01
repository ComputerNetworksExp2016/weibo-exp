from base64 import b64encode
from getpass import getpass
import json
import logging
from pathlib import Path
import pickle

import bs4
from requests import Session

logging.basicConfig(level=logging.DEBUG)

class Post(object):
    """docstring for Post"""
    def __init__(self, uid, created_at, length, reposts, comments, likes):
        self.uid = uid
        self.created_at = created_at
        self.length = length
        self.reposts = reposts
        self.comments = comments
        self.likes = likes

class User(object):
    """docstring for User"""
    def __init__(self, uid, gender, location, posts, followings, followers):
        self.uid = uid
        self.gender = gender
        self.location = location
        self.posts = posts
        self.followings = followings
        self.followers = followers

class Weibo(object):
    """Client for weibo.com."""

    USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E188a Safari/601.1'
    PICKLE_FILE = 'weibo.pickle'

    def __init__(self, username, password):
        """Create a new client."""
        logging.debug('Logging in with the username %s', username)
        self.session = Session()

        payload = {
            'username': username,
            'password': password,
            'savestate': 1,
            'ec': 0,
            'pageerfer': 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
            'entry': 'mweibo'
        }
        headers = {
            'Referer': 'https://passport.weibo.cn/signin/',
            'User-Agent': self.USER_AGENT
        }
        r = self.session.post('https://passport.weibo.cn/sso/login',
                              data=payload, headers=headers)
        r.raise_for_status()

        data = json.loads(r.content.decode())
        if data['retcode'] != 20000000:
            raise RuntimeError('Failed to login: ' + data['msg'])

        self.uid = data['data']['uid']
        logging.info('Logged in, uid: %s', self.uid)

        # Get cross-domain cookies.
        self.session.get(data['data']['loginresulturl']);

        self.users = {}

    def save(self, file=None):
        if file is None:
            file = self.PICKLE_FILE

        logging.debug('Saving to %s.', file)
        pickle.dump(self, open(file, 'wb'))

    @classmethod
    def from_pickle(cls, file=None):
        """Load a client from a pickle file if possible."""
        if file is None:
            file = cls.PICKLE_FILE

        if Path(file).exists():
            logging.debug('Loading from %s.', file)
            return pickle.load(open(file, 'rb'))
        else:
            logging.debug('Pickle file (%s) does not exist, creating new client.', file)
            username = input('Username: ')
            password = getpass('Password for {}: '.format(username))
            return cls(username, password)

    def topic_posts(self, containerid):
        """Return posts of a certain topic."""
        posts = []
        for i in range(2,3):
            r = self.session.get('http://m.weibo.cn/page/pageJson?containerid=%s&page=%d' % (containerid,i))
            r.raise_for_status()
            data = json.loads(r.content.decode())
            l = data['cards'][0]['card_group']
            for j in range(9):
                uid = l[j]['mblog']['id']
                created_at = l[j]['mblog']['created_timestamp']
                length = l[j]['mblog']['textLength']
                reposts = l[j]['mblog']['reposts_count']
                comments = l[j]['mblog']['comments_count']
                likes = l[j]['mblog']['like_count']
                print(uid,created_at,length,reposts,comments,likes)
                posts.append(Post(uid,created_at,length,reposts,comments,likes))
        pass 
    def topic_followers(self, containerid):
        """Return followers of a certain topic."""
        pass

    def user(self, uid):
        """Return a certain user"""
        user = self.users.get(uid)
        if user is None:
            pass

        return user

    def followerings(self, uid):
        """Return following uids"""
        pass


if __name__ == '__main__':
    client = Weibo.from_pickle()
    client.topic_posts('1008086edfd628a87d2ee80e5a4352f13de408')
    client.save()

