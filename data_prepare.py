import re
import requests
import mysql_option as mo
import clean_utils as cc
import codecs
from collections import Counter

MAX_DEPEND_NUM = 50
DATA_PATH = '/home/qiaoyang/pythonProject/Github_Crawler/data_of_tag/'
TAG_SET_FILE = '/home/qiaoyang/pythonProject/Github_Crawler/picked_tag.csv'
FILE_MODE = 'w'
MIN_FREQ = 3


class FileHandler():
    def __init__(self, save_path):
        self.save_path = save_path

    def get_all_file(self, text_name, label_name, file_mode):
        code_all = codecs.open(self.save_path + text_name, file_mode, 'utf8')
        tag_all = codecs.open(self.save_path + label_name, file_mode, 'utf8')
        return code_all, tag_all

    def get_train_file(self, text_name, label_name):
        code_train = codecs.open(self.save_path + text_name, FILE_MODE, 'utf8')
        tag_train = codecs.open(self.save_path + label_name, FILE_MODE, 'utf8')
        return code_train, tag_train

    def get_dev_file(self, text_name, label_name):
        code_dev = codecs.open(self.save_path + text_name, FILE_MODE, 'utf8')
        tag_dev = codecs.open(self.save_path + label_name, FILE_MODE, 'utf8')
        return code_dev, tag_dev

    def get_test_file(self, text_name, label_name):
        code_test = codecs.open(self.save_path + text_name, FILE_MODE, 'utf8')
        tag_test = codecs.open(self.save_path + label_name, FILE_MODE, 'utf8')
        return code_test, tag_test


# get length of texts according to blanks number
def get_length(text):
    return len(str(text).split(' '))


#picked tag set
def get_tag_set():
    tag_set = set()
    tags = codecs.open(TAG_SET_FILE, 'r').read().split('\n')
    for tag in tags:
        tag_set.add(tag)
    return tag_set


#get library or tag list remove unfrequent item
def get_frequet_library(libary_handler):
    if(type(libary_handler) is list):
        texts = '\n'.join(libary_handler).replace('\n', ' ').split(' ')
    else:
        library = libary_handler.read()
        texts = str(library).replace('\n', ' ').split(' ')
    counts = Counter(texts)
    common_list = counts.most_common()
    word_picked = set()
    word_list = []
    word_count = []
    for item in common_list:
        if (item[1] >= MIN_FREQ and item[0] != ''):
            word_picked.add(item[0])
            word_list.append(item[0])
            word_count.append(item[1])

    file = open(DATA_PATH + 'frequecy_library_list.csv', 'w')
    file_map = open(DATA_PATH + 'frequecy_library_list_map.csv', 'w')
    for item in word_picked:
        file.write(item + '\n')
    for tag,count in zip(word_list,word_count):
        file_map.write(tag+","+str(count)+"\n")
    file.close()
    file_map.close()
    return word_picked


#get tag from readme.md according to keyword match
def get_tag_from_readme(tag_set,readme_url):

    request_result = requests.get(readme_url)
    readme = request_result.content.lower()
    tag_result = set()
    if('400: invalid' in readme ):
        return ''
    readmes = re.findall(r"[\w']+|[.,!?;]", readme)
    for r in readmes:
        if(r in tag_set):
            tag_result.add(r)

    print ' '.join(tag_result)
    return ' '.join(tag_result)


# prepare training data
# special char is : . -
def get_data(text_file, label_file, label_is_tag, need_tag_from_readme):
    mysql = mo.Mysql(mo.USER, mo.PWD, mo.DB_NAME, mo.TABLE_NAME)
    result_num = mysql.query_each()
    tag_set = get_tag_set()
    for i in range(result_num):
        result = mysql.cursor.fetchone()
        # get description
        description = cc.data_prepare_clean(str(result[0]))
        # get readme
        readme = cc.data_prepare_clean(str(result[1]))

        # get dependency
        dependecies = []
        if ((result[2] != '') and (result[3] != '')):
            groups = str(result[2]).split('#')
            names = str(result[3]).split('#')
            for group, name in zip(groups, names):
                    dependecies.append(group + ':' + name)
        if (dependecies):
            dependecies = list(set(dependecies))
            dependecies.sort()
        if (len(dependecies) > MAX_DEPEND_NUM):
            dependecies = dependecies[:MAX_DEPEND_NUM]
        dependecy = ' '.join(dependecies).lower().replace('\n', ' ').replace('\t', ' ')

        # get tag
        clean_tags = []
        tags = str(result[4]).split('#')
        for t in tags:
            t = t.lower()
            if(t in tag_set):
                clean_tags.append(t)
        clean_tags.sort()
        tag = ' '.join(clean_tags).lower().replace('\n', ' ').replace('\t', ' ')

        # decide write what kind of info into file
        text = ''
        if (dependecy != '' and (',' not in dependecy) and ('$' not in dependecy)):
            if (description != '' and get_length(description) > 2):
                text = description
            elif (readme != '' and get_length(readme) > 2):
                text = readme
            if (text != ''):
                if (label_is_tag):
                    if(need_tag_from_readme and tag==''):
                        url = str(result[5])
                        tag = get_tag_from_readme(tag_set,url)
                    if(not tag == ''):
                        text_file.write(text + '\n')
                        label_file.write(tag + '\n')
                elif (not label_is_tag):
                    text_file.write(text + '\n')
                    label_file.write(dependecy + '\n')
        print str(i)+'--------'+str(result_num)
    mysql.close_connection()


# split data into train, dev, test data
def train_test_split(is_library, code_all, tag_all, code_train, tag_train, code_dev, tag_dev, code_test, tag_test,
                     dev_percent, test_percent):
    # here you should know in linux wc-l's result is different to len(f.readlines())
    codes = code_all.read().split('\n')
    tags = tag_all.read().split('\n')
    print len(codes)
    print len(tags)
    if(len(codes)==len(tags)):
        dev_number = int(dev_percent * len(codes))
        test_number = int(test_percent * len(codes))
        library_set = get_frequet_library(tags)

        for code, tag, index in zip(codes, tags, range(len(codes))):
            if (is_library):
                new_tag = []
                library = tag.split(' ')
                for l in library:
                    if (l in library_set):
                        new_tag.append(l)
                        print str(len(new_tag)) + '----------' + str(len(str(code).split(' ')))
                tag = ' '.join(new_tag)

            if (tag != ''):
                if (index < test_number):
                    code_test.write(code + '\n')
                    tag_test.write(tag + '\n')
                elif (index < test_number + dev_number):
                    code_dev.write(code + '\n')
                    tag_dev.write(tag + '\n')
                else:
                    code_train.write(code + '\n')
                    tag_train.write(tag + '\n')
                    # print index
    else:
        print("lines are not MATCH!!!")



if __name__ == "__main__":
    handler = FileHandler(DATA_PATH)

    #add new data to file
    # code_all, tag_all = handler.get_all_file('text_all','label_all','a')
    # get_data(code_all, tag_all,True,False)
    # code_all.close()
    # tag_all.close()

    #get frequency list
    code_all, tag_all = handler.get_all_file('text_all', 'label_all', 'r')
    library_set = get_frequet_library(tag_all)
    code_all.close()
    tag_all.close()

    #train test split
    # code_all, tag_all = handler.get_all_file('text_all', 'label_all', 'r')
    # code_train,tag_train = handler.get_train_file('giga-fren.release2.fixed.en','giga-fren.release2.fixed.fr')
    # code_dev,tag_dev = handler.get_dev_file('newstest2013.en','newstest2013.fr')
    # code_test,tag_test = handler.get_test_file('text.test','label.test')
    # train_test_split(False,code_all, tag_all,code_train,tag_train,code_dev,tag_dev,code_test,tag_test,0.1,0.2)
    # code_all.close()
    # tag_all.close()
    # code_train.close()
    # tag_train.close()
    # code_dev.close()
    # tag_dev.close()
    # code_test.close()
    # tag_test.close()
