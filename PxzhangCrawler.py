#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
from bs4 import BeautifulSoup

#访问网页
def pagevisit(url):
	page = urllib.urlopen(url)
	html = page.read()
	soup = BeautifulSoup(html)
	return soup

#提取topics
def gettopics(url):
	soup = pagevisit(url)
	topics = soup.findAll(name="a",attrs={"class":"topic-tag topic-tag-link"})
	for i in range(len(topics)):
		topics[i] = topics[i].string.replace("\n", "").replace(" ", "")
	return topics

#提取readme
def getreadme(url):
	soup = pagevisit(url)
	readme = soup.find(name="article")         #readme所有内容（非string）
	#readme.findAll(name="p")                  #所有正文内容基本都在标签p中，部分是ol、ul标签
	if readme is None:
		return ""
	else:
		return readme.text                         #readme所有内容（string）


#查找文件链接
def nextfiles(soup):
	files = soup.find(name="table",attrs={"class":"files"})
	return files

#提取依赖包
def finddependencies(text, dependencies):
	p = re.compile(r'<artifactId>.*</artifactId>') 
	dependency = p.findall(text)
	for i in range(len(dependency)):
		dependencies.add(dependency[i].replace("<artifactId>","").replace("</artifactId>",""))

def getdependencies(url, last_url, dependencies):
	soup = pagevisit(url)
	next_files = nextfiles(soup)
	#若为文件
	if next_files is None:
		if url.find("pom.xml"):
			pom = soup.find(name="div",attrs={"class":"type-maven-pom"})
			if pom is not None:
				pom_file = pom.text
				finddependencies(pom_file, dependencies)
	#若为文件夹
	else:
		files = next_files.findAll(name="a",attrs={"js-navigation-open"})
		for file in files:
			file_url =  "https://github.com" + file.get('href')
			#考虑到有返回上一目录
			if len(file_url) > len(last_url):               
				#考虑到除了pom.xml，其它文件（有后缀）无用
				if file.get('href').find(".") == -1 or file_url.find("pom.xml") != -1:                
					getdependencies(file_url, url, dependencies)

home_url = "https://github.com/sunjun-group/Ziyuan"#"https://github.com/google/android-classyshark"

topics = gettopics(home_url)                 #最终标签结果
#print topics

readme = getreadme(home_url)                 #最终readme结果
#print readme 

dependencies = set()                         #最终依赖结果
getdependencies(home_url, "", dependencies)
#print dependencies



#files = soup.find(name="table",attrs={"class":"files"}).findAll(name="a",attrs={"js-navigation-open"})


