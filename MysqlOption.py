#!/usr/bin/python
#coding=utf-8
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#according to this tutorial
#http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001391435131816c6a377e100ec4d43b3fc9145f3bb8056000

USER = 'root'
PWD = '1qazxc'
DB_NAME = 'Github'
TABLE_NAME = "raw_data"


def create_database(user, password, database_name):
    conn = MySQLdb.connect(host='localhost', user=user, passwd=password)
    curs = conn.cursor()
    curs.execute("create database " + database_name)
    conn.close()


def create_table(user, password, database_name, table_name):
    conn = MySQLdb.connect(host='localhost', user=user, passwd=password, db=database_name)
    curs = conn.cursor()
    sql = """CREATE TABLE %s (id varchar (255) PRIMARY KEY, project_name TEXT, description TEXT, 
    readme TEXT, library_name TEXT, library_group TEXT,library_version TEXT, git_url TEXT,readme_url TEXT, tag TEXT)"""
    curs.execute(sql % table_name)
    conn.close()


#cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
class mysql():
    def __init__(self,user,password,database_name,table_name):
        self.connection = MySQLdb.connect(host='localhost', user=user, passwd=password, db=database_name)
        self.cursor = self.connection.cursor()
        self.table_name = table_name

    def close_connection(self):
        self.connection.commit()
        self.connection.close()

    def insert(self,data):
        #(id, project_name, description, readme, library_name,library_group,library_version, git_url, origin_id,tag)
        #sql = "'{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}, '{7}', '{8}', '{9}'".format(id, project_name, description, readme, library_name,library_group,library_version, git_url,origin_id, tag)
        sql = "insert into "+ self.table_name+" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,data)


if __name__ == "__main__":
    #create_database(USER,PWD,DB_NAME)
    create_table(USER,PWD,DB_NAME,TABLE_NAME)
    my = mysql(USER,PWD,DB_NAME,TABLE_NAME)
    data = ('2',"34em342","34343","3e434","343ed5","6","8","9",'4','rre f')
    #data = ('1', 'elasticsearch', '', '', '', '', '', 'git://github.com/elastic/elasticsearch.git', '507775', 'elasticsearch#java#search-engine')
    my.insert(data)
    my.close_connection()

