#!/usr/bin/python

#http://morethanseven.net/2007/11/23/archiving-twitter-data-with-python.html
#http://github.com/dudarev/datavis/blob/master/004_twitter_graph/get_timelines.py

"""get timelines (last 100 tweets)
for tweeps from data/members.txt
raw json data is saved to files data/user.txt"""

import tweepy
from get_config import get_config
import os
import sys
import simplejson as json
import yaml

from tweepy.binder import bind_api
from tweepy.parsers import *

class api_raw(tweepy.API):
    """ statuses/user_timeline """
    user_timeline = bind_api(
        path = '/statuses/user_timeline.json',
        payload_type = 'json', payload_list = True,
        allowed_param = ['id', 'user_id', 'screen_name', 'since_id',
                          'max_id', 'count', 'page']
    )

user_name = 'dudarev'

config = get_config()
user = config["twitter_username"]
auth = tweepy.BasicAuthHandler(config["twitter_username"], config["twitter_password"])
api = api_raw(auth)

# os.path.exists('data/%s.json' % user_name):

n_tweets = 830
n_per_page = 100
n_pages = int(n_tweets/n_per_page)+2

last_page = config.get('last_page',0)
max_id = config.get('max_id',None)

load_more = True

while load_more:

    print "max_id = %s" % str(max_id)
    try:
        timeline = api.user_timeline(user_name, count=n_per_page, max_id=max_id)
    except tweepy.TweepError, e: 
        print "error: %s user: %s" % (e,user_name)
        config['max_id'] = max_id
        fp = open('config.yaml','w')
        yaml.dump(config, fp)
        fp.close()
        sys.exit()

    if timeline:
        for t in timeline:
            file_tweet = open('data/%s.json' % t['id'],'w')
            file_tweet.write(json.dumps(t))
            file_tweet.close()
            print t['id']
        print len(timeline), 'tweets'
        print
        max_id = timeline[-1]['id']
    else:
        print 'no tweets'
        load_more = False
