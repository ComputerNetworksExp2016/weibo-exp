from base64 import b64encode
from datetime import datetime, timedelta
from time import sleep
from getpass import getpass
import json
import logging
from pathlib import Path
import pickle

from bs4 import BeautifulSoup
from requests import Session

logging.basicConfig(level=logging.DEBUG)

def parse_num(s):
    if s[-1] == '万':
        return int(s[:-1]) * 10000
    else:
        return int(s)

class Post(object):
    """docstring for Post"""
    def __init__(self, mid, uid, created_at, length, repost_num, comment_num, like_num):
        self.mid = mid
        self.uid = uid
        self.created_at = created_at
        self.length = length
        self.repost_num = repost_num
        self.comment_num = comment_num
        self.like_num = like_num


    def __str__(self):
        return 'Post({}, {}, {}, {}, {}, {}, {})'.format(
            self.mid, self.uid, self.created_at, self.length, self.repost_num,
            self.comment_num, self.like_num)

class User(object):
    """docstring for User"""
    def __init__(self, uid, gender, age, location, post_num, following_num, follower_num, following_uids):
        self.uid = uid
        self.gender = gender
        self.age = age
        self.location = location
        self.post_num = post_num
        self.following_num = following_num
        self.follower_num = follower_num
        self.following_uids = following_uids

    def __str__(self):
        return 'User({}, {}, {}, {}, {}, {}, {}, {})'.format(
            self.uid, self.gender, self.age, self.location, self.post_num,
            self.following_num, self.follower_num, self.following_uids)

class Weibo(object):
    """Client for weibo.com."""

    USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13E188a Safari/601.1'
    PICKLE_FILE = 'weibo.pickle'
    REQUEST_INTERVAL = 0.5

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
        }
        r = self.post('https://passport.weibo.cn/sso/login',
                      data=payload, headers=headers)
        r.raise_for_status()

        data = json.loads(r.content.decode())
        if data['retcode'] != 20000000:
            raise RuntimeError('Failed to login: ' + data['msg'])

        self.uid = data['data']['uid']
        logging.info('Logged in, uid: %s', self.uid)

        # Get cross-domain cookies.
        self.get(data['data']['loginresulturl']);

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

    def get(self, url, **kw):
        if 'headers' not in kw:
            kw['headers'] = {}
        kw['headers']['User-Agent'] = self.USER_AGENT

        sleep(self.REQUEST_INTERVAL)
        return self.session.get(url, **kw)

    def post(self, url, **kw):
        if 'headers' not in kw:
            kw['headers'] = {}
        kw['headers']['User-Agent'] = self.USER_AGENT

        sleep(self.REQUEST_INTERVAL)
        return self.session.post(url, **kw)

    def topic_posts(self, containerid):
        """Return posts of a certain topic."""
        for i in range(2, 101):
            failure = 0
            while failure < 3:
                try:
                    r = self.get('http://m.weibo.cn/page/pageJson?containerid=%s&page=%d' % (containerid, i))
                    r.raise_for_status()
                    data = json.loads(r.content.decode())
                    l = data['cards'][0]['card_group']
                    for j in l:
                        mid = j['mblog']['id']
                        uid = j['mblog']['user']['id']
                        created_at = datetime.fromtimestamp(j['mblog']['created_timestamp'])
                        length = j['mblog']['textLength']
                        repost_num = j['mblog']['reposts_count']
                        comment_num = j['mblog']['comments_count']
                        like_num = j['mblog']['like_count']
                        yield Post(mid, uid, created_at, length, repost_num, comment_num, like_num)
                    break
                except Exception as e:
                    logging.error(e)
                    failure += 1
            else:  # Failed to fetch more posts.
                break
        raise StopIteration()


    def topic_followers(self, containerid):
        """Return followers of a certain topic."""
        followers_id = []
        for i in range(2, 501):
            failure = 0
            while failure < 3:
                try:
                    r = self.get('http://m.weibo.cn/page/pageJson?&containerid=230403_-_%s&page=%d' % (containerid, i))
                    r.raise_for_status()
                    data = json.loads(r.content.decode())
                    l = data['cards'][0]['card_group']
                    for j in l:
                        yield j['user']['id']
                    break
                except Exception as e:
                    logging.error(e)
                    failure += 1
            else:  # Failed to fetch more posts.
                break
        raise StopIteration()

    def user(self, uid):
        """Return a certain user"""
        failure = 0
        while failure < 3:
            try:
                r = self.get('http://m.weibo.cn/u/{}'.format(uid))
                r.raise_for_status()

                data = r.content.decode()
                begin = data.find("""[{"mod_type":""")
                end = data.find("""},'common':""")
                body = data[begin:end]
                body = json.loads(body)
                post_num = int(body[1]['mblogNum'])
                following_num = int(body[1]['attNum'])
                follower_num = int(body[1]['fansNum'])

                # print(r.content)
                # soup = BeautifulSoup(r.content.decode(), "html.parser")
                # infos = soup.select('.mct-a.txt-s')
                # post_num = parse_num(infos[2].get_text())
                # following_num = parse_num(infos[4].get_text())
                # follower_num = parse_num(infos[8].get_text())

                r = self.get('http://m.weibo.cn/users/{}'.format(uid))
                r.raise_for_status()
                soup = BeautifulSoup(r.content.decode(), "html.parser")

                infos = {}
                for name, value in zip(soup.select('.item-info-page span'),
                                       soup.select('.item-info-page p')):
                    infos[name.get_text()] = value.get_text()

                gender = infos.get('性别')
                location = infos.get('所在地')
                birthday = infos.get('生日')
                if birthday is None:
                    age = None
                else:
                    try:
                        birthday = datetime.strptime(birthday, '%Y-%m-%d')
                        if birthday == datetime(1970, 1, 1):
                            age = None
                        else:
                            age = (datetime.today() - birthday) / timedelta(365)
                    except ValueError:
                        age = None


                following_uids = []
                for following_uid in self.followings(uid):
                    following_uids.append(following_uid)

                return User(uid, gender, age, location, post_num, following_num, follower_num, following_uids)
            except Exception as e:
                logging.error(e)
                failure += 1
        return None

    def followings(self, uid):
        """Return following uids"""
        followingsID = []
        i = 1
        while True:
            failure = 0
            while failure < 3:
                try:
                    r = self.get('http://m.weibo.cn/page/json?containerid=100505%s_-_FOLLOWERS&page=%d' % (uid, i))
                    r.raise_for_status()
                    data = json.loads(r.content.decode())
                    l = data['cards'][0]['card_group']
                    for j in l:
                        yield j['user']['id']
                    break
                except Exception as e:
                    logging.error(e)
                    failure += 1
            else:
                break
            i = i + 1;
        raise StopIteration()


if __name__ == '__main__':
    client = Weibo.from_pickle()
    # client.topic_posts('1008086edfd628a87d2ee80e5a4352f13de408')
    # client.save()
    # print(client.user('5324474591'))
    # print(followingsID)
    # for post in client.topic_posts('1008086edfd628a87d2ee80e5a4352f13de408'):
    #     print(post)
    for user in client.topic_followers('1008086edfd628a87d2ee80e5a4352f13de408'):
        print(user)
