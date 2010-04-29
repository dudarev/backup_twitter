#!/usr/bin/python
import os
import simplejson as json
import dateutil.parser

tweets = []

for root, dirs, files in os.walk('data'):
    for file in files:
        print file
        data = json.loads(open(os.path.join(root, file)).read())
        text = data['text']
        time = dateutil.parser.parse(data['created_at'])
        tweets.append( (time, text) )

tweets.sort(reverse=True)

f = open('tweets.txt','w')
for t in tweets:
    f.write('%s\n\n' % t[1].encode('utf8'))
