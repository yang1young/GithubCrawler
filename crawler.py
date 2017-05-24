#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')
import json, requests

TOKEN = '5e507923a11636aa1c7d99b3118e7fc41600a26d'
MAX_PAGE = 1
ITEM_PER_PAGE = 3


def mytest():
    page = '3'
    url = "https://api.github.com/search/repositories?q=language:Java&per_page=10&page="+page#+"&access_token="+TOKEN
    payload = {"Accept":"application/vnd.github.mercy-preview+json","Authorization": "token "+TOKEN}
    #url = 'https://api.github.com/repos/libgdx/libgdx'
    a = requests.get(url,headers=payload)
    res = json.loads(a.content)
    dict_res = dict(res)
    print res

    #     if(dict_item.get("name")=='android-classyshark'):
    #           for i, j in dict(item).iteritems():
    #               print str(i)+':'+str(j)


def get_information(item):

    dict_item = dict(item)
    project_name = dict_item.get("name")
    url =  dict_item.get("url")
    git_url = dict_item.get("git_url")
    payload = {"Accept":"application/vnd.github.mercy-preview+json","Authorization": "token "+TOKEN}
    res = dict(json.loads(requests.get(url,headers=payload).content))
    topics = res.get('topics')
    print project_name,git_url,topics


def crawl_url():
    id = 0
    for i in range(MAX_PAGE):
        id +=1
        url = "https://api.github.com/search/repositories?q=language:Java&per_page="+ str(ITEM_PER_PAGE)+"&page="+ str(i) + "&access_token=" + TOKEN
        res = json.loads(requests.get(url).content)
        items = dict(res).get("items")
        for item in items:
            get_information(item)





crawl_url()
#mytest()