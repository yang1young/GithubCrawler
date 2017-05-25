#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import CleanUtils as cu
reload(sys)
sys.setdefaultencoding('utf-8')
import json, requests
import MysqlOption as mysql
#update your token here, https://github.com/settings/tokens
TOKEN = '2627031bf3c660b85dc3637d58a38b11b47cba6e'
#query limit is 30 times per hour
MAX_PAGE = 4
#max is 100 record per page
ITEM_PER_PAGE = 10

TYPE = ['README.md','build.gradle','pom.xml']

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
    file_path = []

    get_file_url = project_url+'/git/trees/master?recursive=1'
    file_result = json.loads(requests.get(get_file_url).content)
    if(dict(file_result).has_key('tree')):
        for r in dict(file_result).get('tree'):
            r = dict(r)
            if (r.get('type') == 'blob'):
                for type_choose in TYPE:
                    if (type_choose in str(r.get('path'))):
                        #blob_url = "https://raw.githubusercontent.com/"+full_name + '/master/' + r.get('path')
                        file_path.append(str(r.get('path')))
    #print file_path
    # print project_name,git_url,topics,description,origin_id,file_urls
    # print '************************************************************'
    return project_name,git_url,topics,description,origin_id,file_path,project_url


#extract readme and dependency from url
def extract_info_from_file(project_url,file_paths):
    readme = ''

    #format is groupId:artifactId:version
    # eg, com.android.tools.build:gradle:1.2.3, split by :
    dependency = []

    dependency_group = []
    dependency_name = []
    dependency_version = []

    for path in file_paths:
        #readme = cu.extract_markdown(readme)
        pass

    for depend in dependency:
        infos = str(depend).split(":")
        dependency_group.append(infos[0])
        dependency_name.append(infos[1])
        dependency_version.append(infos[2])

    return readme,dependency,'#'.join(dependency_group),'#'.join(dependency_name),'#'.join(dependency_version)


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
            project_name, git_url, topics, description, origin_id, file_path,project_url = get_information(item)
            if(not len(file_path)==0):
                readme, dependency,group,name,version = extract_info_from_file(project_url,file_path)
                if(not(description=='' and readme=='')):
                    description = cu.clean(description)
                    readme = cu.clean(readme)
                    if(need_insert_database):
                        id += 1
                        data = (str(id),str(project_name),str(description),readme,name,group,version,git_url,str(origin_id),topics)
                        print data
                        mysql_handler.insert(data)
                        mysql_handler.connection.commit()
                    else:
                        print readme



if __name__=="__main__":
    crawl_url(False)
    #mytest()