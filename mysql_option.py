#!/usr/bin/python
# coding=utf-8
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

# for mysql use
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
    sql = """CREATE TABLE %s (id varchar (255) PRIMARY KEY, project_name varchar (255), description TEXT,
    readme TEXT, library_name TEXT, library_group TEXT,library_version TEXT, git_url varchar (255),readme_url varchar (255),
    create_date varchar (255),update_date varchar (255),tag TEXT)"""
    curs.execute(sql % table_name)
    conn.close()


# cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
class Mysql():
    def __init__(self, user, password, database_name, table_name):
        self.connection = MySQLdb.connect(host='localhost', user=user, passwd=password, db=database_name)
        self.cursor = self.connection.cursor()
        self.table_name = table_name

    def close_connection(self):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def insert(self, data):
        # (id, project_name, description, readme, library_name,library_group,library_version, git_url, origin_id,tag)
        sql = "insert into " + self.table_name + " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, data)

    def query_all(self):
        sql = "select description,readme,library_group,library_name, tag from " + self.table_name + " where not description = '' OR not readme = '' "
        self.cursor.execute(sql)
        values = self.cursor.fetchall()
        return values

    def query_each(self):
        sql = "select description,readme,library_group,library_name, tag, readme_url from " + self.table_name + " where not description = '' OR not readme = '' "
        self.cursor.execute(sql)
        value_num = self.cursor.rowcount
        return value_num


if __name__ == "__main__":
    create_database(USER, PWD, DB_NAME)
    create_table(USER, PWD, DB_NAME, TABLE_NAME)
    # my = mysql(USER,PWD,DB_NAME,TABLE_NAME)
    # data = ('2',"34em342","34343","3e434","343ed5","6","8","9",'4','rre f')
    # my.insert(data)
    # my.close_connection()
