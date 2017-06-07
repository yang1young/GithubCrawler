import mysql_option as mo
import clean_utils as cc
import codecs
MAX_DEPEND_NUM = 10
DATA_PATH = ''

#prepare training data
#special : . -
def get_data():
    mysql = mo.Mysql(mo.USER,mo.PWD,mo.DB_NAME,mo.TABLE_NAME)
    result_num = mysql.query_each()
    for i in range(result_num):
        result = mysql.cursor.fetchone()
        description = cc.data_prepare_clean(str(result[0]))
        readme = cc.data_prepare_clean(str(result[1]))
        dependecies = []
        if((result[2]!='') and (result[3]!='')):
            groups = str(result[2]).split('#')
            names = str(result[3]).split('#')
            for group,name in zip(groups,names):
                if(name!='gradle' and name!='junit'):
                    dependecies.append(group+':'+name)
        if(dependecies):
            dependecies = list(set(dependecies))
            dependecies.sort()
        if(len(dependecies)>10):
            dependecies = dependecies[:10]

        dependecy = ' '.join(dependecies)
        tags = str(result[4]).split('#')
        tags.sort()
        tag = ' '.join(tags)
        print description
    mysql.close_connection()

def data_to_file(save_path):
    code_train = codecs.open(save_path + 'code.train', 'w+', 'utf8')
    tag_train = codecs.open(save_path + 'tag.train', 'w+', 'utf8')

    code_dev = codecs.open(save_path + 'code.dev', 'w+', 'utf8')
    tag_dev = codecs.open(save_path + 'tag.dev', 'w+', 'utf8')

    code_test = codecs.open(save_path + 'code.test', 'w+', 'utf8')
    tag_dev = codecs.open(save_path + 'tag.test', 'w+', 'utf8')



if __name__ == "__main__":
    get_data()