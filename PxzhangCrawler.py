import urllib
import re
from bs4 import BeautifulSoup

#访问网页
def pagevisit(url):
	page = urlib.urlopen(url)
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

def getdependencies(url, dependencies):
	soup = pagevisit(url)
	next_files = nextfiles(soup)
	#若为文件
	if next_files is None:
		if url.find("pom.xml"):
			pom = soup.find(name="div",attrs={"class":"type-maven-pom"}).text
			finddependencies(pom, dependencies)
	#若为文件夹
	else
		files = next_files.findAll(name="a",attrs={"js-navigation-open"})
		for file in files:
			traversalfiles("https://github.com" + file.get('href'))

home_url = "https://github.com/google/android-classyshark"
dependencies = set()                         #最终依赖结果
getdependencies(home_url, dependencies)
topics = gettopics(home_url)                 #最终标签结果
readme = getreadme(home_url)                 #最终readme结果



#files = soup.find(name="table",attrs={"class":"files"}).findAll(name="a",attrs={"js-navigation-open"})


