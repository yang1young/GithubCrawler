#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib
from bs4 import BeautifulSoup


# visit html when giving a url
def pagevisit(url):
    page = urllib.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html)
    return soup


# get topics from html page
def gettopics(url):
    soup = pagevisit(url)
    topics = soup.findAll(name="a", attrs={"class": "topic-tag topic-tag-link"})
    for i in range(len(topics)):
        topics[i] = topics[i].string.replace("\n", "").replace(" ", "")
    return topics


# get readme file
def getreadme(url):
    soup = pagevisit(url)
    readme = soup.find(name="article")
    if readme is None:
        return ''
    else:
        return readme.text

# find files
def nextfiles(soup):
    files = soup.find(name="table", attrs={"class": "files"})
    return files


# extract dependency from pom.xml
def extract_dependencies(text, dependencies):
    p = re.compile(r'<artifactId>.*</artifactId>')
    dependency = p.findall(text)
    for i in range(len(dependency)):
        dependencies.add(dependency[i].replace("<artifactId>", "").replace("</artifactId>", ""))


# get all pom.xml
def get_dependencies(url, last_url, dependencies):
    soup = pagevisit(url)
    next_files = nextfiles(soup)
    # if not file dir
    if next_files is None:
        if url.find("pom.xml"):
            pom = soup.find(name="div", attrs={"class": "type-maven-pom"})
            if pom is not None:
                pom_file = pom.text
                extract_dependencies(pom_file, dependencies)
    # if is file dir
    else:
        files = next_files.findAll(name="a", attrs={"js-navigation-open"})
        for file in files:
            file_url = "https://github.com" + file.get('href')
            if len(file_url) > len(last_url):
                # remove other files
                if file.get('href').find(".") == -1 or file_url.find("pom.xml") != -1:
                    get_dependencies(file_url, url, dependencies)


if __name__ == "__main__":
    home_url = "https://github.com/sunjun-group/Ziyuan"  # "https://github.com/google/android-classyshark"
    topics = gettopics(home_url)  # get topics
    readme = getreadme(home_url)  # get readme text
    dependencies = set()  # get dependencies
    get_dependencies(home_url, "", dependencies)
