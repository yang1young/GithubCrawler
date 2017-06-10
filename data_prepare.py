import mysql_option as mo
import clean_utils as cc
import codecs

MAX_DEPEND_NUM = 20
DATA_PATH = '/home/yang/PythonProject/Github_Crawler/data/'
FILE_MODE = 'w'

class FileHandler():

    def __init__(self, save_path):
        self.save_path = save_path

    def get_all_file(self, text_name, label_name, file_mode):
        code_all = codecs.open(self.save_path + text_name, file_mode, 'utf8')
        tag_all = codecs.open(self.save_path + label_name, file_mode, 'utf8')
        return code_all, tag_all

    def get_train_file(self,text_name,label_name):
        code_train = codecs.open(self.save_path + text_name, FILE_MODE, 'utf8')
        tag_train = codecs.open(self.save_path + label_name, FILE_MODE, 'utf8')
        return code_train,tag_train

    def get_dev_file(self,text_name,label_name):
        code_dev = codecs.open(self.save_path + text_name, FILE_MODE, 'utf8')
        tag_dev = codecs.open(self.save_path + label_name, FILE_MODE, 'utf8')
        return code_dev,tag_dev

    def get_test_file(self,text_name,label_name):
        code_test = codecs.open(self.save_path + text_name, FILE_MODE, 'utf8')
        tag_test = codecs.open(self.save_path + label_name, FILE_MODE, 'utf8')
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
        if(len(dependecies)>MAX_DEPEND_NUM):
            dependecies = dependecies[:MAX_DEPEND_NUM]
        dependecy = ' '.join(dependecies).lower().replace('\n',' ')

        #get tag
        tags = str(result[4]).split('#')
        tags.sort()
        tag = ' '.join(tags).lower().replace('\n',' ')

        #decide write what kind of info into file
        text = ''
        if(dependecy!='' and (',' not in dependecy)and ('$' not in dependecy)):
            if(description != '' and get_length(description)>2):
                text = description
            elif(readme !=''and get_length(readme)>2):
                text = readme
            if(text != ''):
                if (label_is_tag and not tag == ''):
                    text_file.write(text+'\n')
                    label_file.write(tag+'\n')
                elif(not label_is_tag):
                    text_file.write(text+'\n')
                    label_file.write(dependecy+'\n')

    mysql.close_connection()

# split data into train, dev, test data
def train_test_split( code_all, tag_all,code_train,tag_train,code_dev,tag_dev,code_test,tag_test,dev_percent,test_percent):
    #here you should know in linux wc-l's result is different to len(f.readlines())
    codes = code_all.read().split('\n')
    tags = tag_all.read().split('\n')
    print len(codes)
    print len(tags)
    dev_number = int(dev_percent*len(codes))
    test_number = int(test_percent*len(codes))
    for code,tag,index in zip(codes,tags,range(len(codes))):
        if(index<test_number):
            code_test.write(code+'\n')
            tag_test.write(tag+'\n')
        elif(index<test_number+dev_number):
            code_dev.write(code+'\n')
            tag_dev.write(tag+'\n')
        else:
            code_train.write(code+'\n')
            tag_train.write(tag+'\n')
        print index



if __name__ == "__main__":
    handler = FileHandler(DATA_PATH)
    # code_all, tag_all = handler.get_all_file('text_all','label_all','w')
    # get_data(code_all, tag_all,False)
    # code_all.close()
    # tag_all.close()

    code_all, tag_all = handler.get_all_file('text_all', 'label_all', 'r')
    code_train,tag_train = handler.get_train_file('text.train','label.train')
    code_dev,tag_dev = handler.get_dev_file('text.dev','label.dev')
    code_test,tag_test = handler.get_test_file('text.test','label.test')
    train_test_split( code_all, tag_all,code_train,tag_train,code_dev,tag_dev,code_test,tag_test,0.05,0.2)
    code_all.close()
    tag_all.close()
    code_train.close()
    tag_train.close()
    code_dev.close()
    tag_dev.close()
    code_test.close()
    tag_test.close()



