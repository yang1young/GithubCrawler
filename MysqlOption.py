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
    sql = """CREATE TABLE %s (id varchar (255) PRIMARY KEY, project_name varchar (255), description varchar(255), readme TEXT, library TEXT, tag TEXT)"""
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
        sql = "insert into "+self.table_name+"(id, project_name, description, readme, library, tag) values(%s,%s,%s,%s,%s,%s)"%data
        self.cursor.execute(sql)


if __name__ == "__main__":
    #create_database(USER,PWD,DB_NAME)
    #create_table(USER,PWD,DB_NAME,TABLE_NAME)
    my = mysql(USER,PWD,DB_NAME,TABLE_NAME)
    data = ('1','2','3','4','5','6')
    my.insert(data)
    my.close_connection()

