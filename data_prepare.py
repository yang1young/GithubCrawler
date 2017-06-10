import mysql_option as mo
import clean_utils as cc
import codecs
MAX_DEPEND_NUM = 10
DATA_PATH = '/home/yang/PythonProject/Github_Crawler/data/'


class FileHandler():

    def __init__(self, save_path):
        self.save_path = save_path

    def get_train_file(self,text_name,label_name):
        code_train = codecs.open(self.save_path + text_name, 'w', 'utf8')
        tag_train = codecs.open(self.save_path + label_name, 'w', 'utf8')
        return code_train,tag_train

    def get_dev_file(self,text_name,label_name):
        code_dev = codecs.open(self.save_path + text_name, 'a', 'utf8')
        tag_dev = codecs.open(self.save_path + label_name, 'a', 'utf8')
        return code_dev,tag_dev

    def get_test_file(self,text_name,label_name):
        code_test = codecs.open(self.save_path + text_name, 'a', 'utf8')
        tag_test = codecs.open(self.save_path + label_name, 'a', 'utf8')
        return code_test,tag_test


#get length of texts according to blanks number
def get_length(text):
    return len(str(text).split(' '))


#prepare training data
#special char is : . -
def get_data(text_file, label_file,label_is_tag):

    mysql = mo.Mysql(mo.USER,mo.PWD,mo.DB_NAME,mo.TABLE_NAME)
    result_num = mysql.query_each()
    for i in range(result_num):
        result = mysql.cursor.fetchone()
        #get description
        description = cc.data_prepare_clean(str(result[0]))
        #get readme
        readme = cc.data_prepare_clean(str(result[1]))

        #get dependency
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

        #get tag
        tags = str(result[4]).split('#')
        tags.sort()
        tag = ' '.join(tags)

        #decide write what kind of info into file
        text = ''
        if(dependecy!='' and (',' not in dependecy)and ('$' not in dependecy)):
            if(description != '' and get_length(description)>2):
                text = description
            elif(readme !=''and get_length(readme)>2):
                text = readme
            else:
                continue
            if (label_is_tag and not tag == ''):
                text_file.write(text+'\n')
                label_file.write(tag+'\n')
            elif(not label_is_tag):
                text_file.write(text+'\n')
                label_file.write(dependecy+'\n')

    mysql.close_connection()



if __name__ == "__main__":
    handler = FileHandler(DATA_PATH)
    code_train, tag_train = handler.get_train_file('train', 'label')
    get_data(code_train, tag_train,False)
    code_train.close()
    tag_train.close()