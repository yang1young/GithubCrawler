# Github_Crawler
crawl github data using API then store into database

## you need to install:
* Python2.7 (better Anaconda)
* mysql, according to this tutorial
http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001391435131816c6a377e100ec4d43b3fc9145f3bb8056000


## user guide
following steps:
1. generate your github access token, following this https://github.com/settings/tokens
2. mkdir a new file in the project path named token_key, then copy&paste your personal access token into it(no need to add \n)
3. modify MysqlOption.py and set your mysql USER and PASSWORD
4. run MysqlOption.py to create database and new table
5. modify GithubCrawl.py ,set START_FROM_TIME = YOUR START, since the project count is 320W and
   every query max return result is 1000, we need to split these result according to create time
6. happily run GithubCrawl.py

