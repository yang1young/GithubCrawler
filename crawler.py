#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json, requests

token = 'a632afd558411ee249ad7d80f083f44e2a47c5fb'
#url = "https://api.github.com/repositories?since=" + since+"?q=language:Java&sort=stars&order=desc"
page = '3'
url = "https://api.github.com/search/repositories?q=language:Java&per_page=100&page="+page+"&access_token="+token
res = json.loads(requests.get(url).content)
items = dict(res).get("items")

for item in items:

    dict_item = dict(item)
    if(dict_item.get("name")=='android-classyshark'):
        for i, j in dict(item).iteritems():
            print str(i)+':'+str(j)

#print json.loads(requests.get("https://api.github.com/rate_limit?access_token="+token).content)
