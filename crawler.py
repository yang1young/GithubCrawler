#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import json, requests

#update your token here, https://github.com/settings/tokens
TOKEN = ''
#query limit is 30 times per hour
MAX_PAGE = 4
#max is 100 record per page
ITEM_PER_PAGE = 100

#just for test
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

    #do another query for a specific project and modify GET header,query limits is 5000 per hour
    head = {"Accept":"application/vnd.github.mercy-preview+json","Authorization": "token "+TOKEN}
    res = dict(json.loads(requests.get(url,headers=head).content))
    origin_id = res.get('id')
    topics = res.get('topics')
    description = res.get('description')

    print project_name,git_url,topics,description,origin_id


def crawl_url():
    id = 0
    #crawl according to pages
    for i in range(MAX_PAGE):
        id +=1
        url = "https://api.github.com/search/repositories?q=language:Java&per_page="+ str(ITEM_PER_PAGE)+"&page="+ str(i) + "&access_token=" + TOKEN
        request_result = requests.get(url)
        print request_result.headers.get('X-RateLimit-Remaining')
        res = json.loads(request_result.content)
        items = dict(res).get("items")
        #every page has several project
        for item in items:
            get_information(item)





crawl_url()
#mytest()