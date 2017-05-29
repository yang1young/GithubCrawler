#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import re
from bs4 import BeautifulSoup
import sys
import CleanUtils as cu
reload(sys)
sys.setdefaultencoding('utf-8')
import json, requests
import MysqlOption as mysql
#update your token here, https://github.com/settings/tokens
TOKEN = 'deab18031b619c12708606ad60077a9358f4c4f5'
#query limit is 30 times per hour
MAX_PAGE = 10
#max is 100 record per page
ITEM_PER_PAGE = 30

TYPE = ['README','build.gradle','pom.xml']

#just for test
def mytest():
    page = '3'
    #url = "https://api.github.com/search/repositories?q=language:Java&per_page=10&page="+page#+"&access_token="+TOKEN
    payload = {"Accept":"application/vnd.github.mercy-preview+json","Authorization": "token "+TOKEN}
    #url = 'https://api.github.com/repos/json-iterator/java/git/trees/master?recursive=1'
    url = 'https://api.github.com/repos/ReactiveX/RxJava/git/trees/master?recursive=1'
    a = requests.get(url,headers=payload)
    res = json.loads(a.content)
    for r in dict(res).get('tree'):
        r = dict(r)
        if(r.get('type')=='blob'):
            for type_choose in TYPE:
                if(type_choose in str(r.get('path'))):
                     blob_url = "https://raw.githubusercontent.com/json-iterator/java/"+'master/'+r.get('path') #'/'.join(r.get('url').split('/')[:-3])+'/'+'blob/master/'+r.get('path')
                     print blob_url


#extract information of single project
def get_information(item):

    dict_item = dict(item)
    project_name = dict_item.get("name")
    project_url =  dict_item.get("url")
    git_url = dict_item.get("git_url")

    #do another query for a specific project and modify GET header,query limits is 5000 per hour
    head = {"Accept":"application/vnd.github.mercy-preview+json","Authorization": "token "+TOKEN}
    res = dict(json.loads(requests.get(project_url,headers=head).content))
    origin_id = res.get('id')
    topics = '#'.join(res.get('topics'))
    description = res.get('description')
    full_name = res.get('full_name')
    file_urls = []
    get_file_url = project_url+'/git/trees/master?recursive=1'
    file_result = json.loads(requests.get(get_file_url,headers=head).content)

    if(dict(file_result).has_key('tree')):
        for r in dict(file_result).get('tree'):
            r = dict(r)
            if (r.get('type') == 'blob'):
                for type_choose in TYPE:
                    temp_path = str(r.get('path'))
                    if (type_choose in temp_path):
                        blob_url = "https://raw.githubusercontent.com/"+full_name + '/master/' + r.get('path')
                        file_urls.append(blob_url)
    #print file_path
    # print project_name,git_url,topics,description,origin_id,file_urls
    # print '************************************************************'
    return project_name,git_url,topics,description,origin_id,file_urls


#extract readme and dependency from url
def extract_info_from_file(urls):
    readme = ''

    #format is groupId:artifactId:version
    # eg, com.android.tools.build:gradle:1.2.3, split by :
    dependency = []

    dependency_group = []
    dependency_name = []
    dependency_version = []

    for url in urls:
        #readme = cu.extract_markdown(readme)
        page = urllib.urlopen(url)
        text = page.read()
        #README.md
        if url.find(TYPE[0]) != -1:
            readme = cu.extract_markdown(text)
        #build.gradle
        elif url.find(TYPE[1]) != -1:
            index = text.find("dependencies {")
            text = text[index:]
            index = text.find("}")
            text = text[:index]
            p = re.compile(r'\'(.*:.*:.*)\'\n')
            for dep in p.findall(text):
                dependency.append(dep)
        #pom.xml
        elif url.find(TYPE[2]) != -1:
            soup = BeautifulSoup(text, "lxml")
            dep = soup.findAll(name = "dependency")
            for i in range(len(dep)):
                temp = dep[i].contents
                if(len(temp)==7):
                    dependency.append(temp[1].text + ":" + temp[3].text + ":" + temp[5].text)
 
    for depend in dependency:
        infos = str(depend).split(":")
        dependency_group.append(infos[0])
        dependency_name.append(infos[1])
        dependency_version.append(infos[2])

    return readme,dependency,'#'.join(dependency_group),'#'.join(dependency_name),'#'.join(dependency_version)


def get_real_file_url(urls):
    min_readme_lenghth = 100000
    min_readme_path = ''
    for url in urls:
        if('README' in url):
            if(len(url)<min_readme_lenghth):
                min_readme_lenghth = len(url)
                min_readme_path = url
    new_urls = []
    for url in urls:
        if (not('README' in url)):
            new_urls.append(url)
    new_urls.sort(lambda x,y: cmp(len(str(x).split('/')), len(str(x).split('/'))))
   # print new_urls
    new_urls = new_urls[:10]

    new_urls.append(min_readme_path)
    return new_urls,min_readme_path



#main function
def crawl_url(need_insert_database):
    id = 0
    if(need_insert_database):
        mysql_handler = mysql.mysql(mysql.USER,mysql.PWD,mysql.DB_NAME,mysql.TABLE_NAME)

    #crawl according to pages
    for i in range(MAX_PAGE):
        url = "https://api.github.com/search/repositories?q=language:Java&per_page="+ str(ITEM_PER_PAGE)+"&page="+ str(i+1) + "&access_token=" + TOKEN
        request_result = requests.get(url)
        print request_result.headers.get('X-RateLimit-Remaining')
        res = json.loads(request_result.content)
        items = dict(res).get("items")
        #every page has several project
        #readme, dependency, group, name, version = '',[],'','',''
        for item in items:
            project_name, git_url, topics, description, origin_id, file_urls = get_information(item)
            #print file_urls
            if(not len(file_urls)==0):
                file_urls,readme_url = get_real_file_url(file_urls)
                readme, dependency,group,name,version = extract_info_from_file(file_urls)
                if(not(description=='' and readme=='')):
                    description = cu.clean(description)
                    readme = cu.clean(readme)
                    if(need_insert_database):
                        id += 1
                        data = (str(origin_id),str(project_name),str(description),readme,name,group,version,git_url,readme_url,topics)
                        #print data
                        print str(id)+'-----------'+str(i)+'---------'+project_name+'--------'
                        try:
                            mysql_handler.insert(data)
                            mysql_handler.connection.commit()
                        except:
                            print 'Duplicate entry'
                    else:
                        print readme



if __name__=="__main__":
    crawl_url(True)
    #mytest()