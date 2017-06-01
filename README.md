# Github_Crawler
crawl github data using API then store into database

## you need to install:
* Python2.7 (better Anaconda)
* mysql, you can install and configure according to this tutorial
http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001391435131816c6a377e100ec4d43b3fc9145f3bb8056000

## file introduction
1. CrawlerWithoutAPI.py
   demo crwal github without API, give a URL of REPO then return result
2. GithubCrawler.py
   crawl github using API, search all java project and extract readme,description,topic and all dependency file from .gradle and .pom
3. MysqlOption.py
   Mysql option, create database, table and insert/search
4. CleanUtils.py
   Some tools to do cleaning and extraction
5. token_key
   your Github API token

## user guide
following steps:
1. generate your github access token, following this https://github.com/settings/tokens
2. mkdir a new file in the project path named token_key, then copy&paste your personal access token into it(no need to add \n)
3. modify MysqlOption.py and set your mysql USER and PASSWORD
4. run MysqlOption.py to create database and new table
5. modify GithubCrawl.py ,set START_FROM_TIME = YOUR START,set END_TO_TIME = YOUR END, set SRART_FROM_PAGE = YOUR START
   since the return project count is 320W and every query total max return result is 1000, and for once time,
   max return result is 100,so firstly we need to split these result according to repo create time, ensure every query
   total return result is less than 1000, for every specific time period, we need to split the result(max is 1000)
   into page so we can get all result
6. happily run GithubCrawl.py

### if you think this project may helpful, may you give my repo a STAR? :)

