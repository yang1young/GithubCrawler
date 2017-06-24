import mysql_option as mo
import clean_utils as cc
import codecs
from collections import Counter

MAX_DEPEND_NUM = 50
DATA_PATH = '/home/qiaoyang/pythonProject/Github_Crawler/data_of_tag/'
FILE_MODE = 'w'
MIN_FREQ = 0


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


def get_frequet_library(libary_handler):
    library = libary_handler.read()
    texts = str(library).replace('\n', ' ').split(' ')
    counts = Counter(texts)
    common_list = counts.most_common()
    word_picked = set()
    for item in common_list:
        if (item[1] >= MIN_FREQ and item[0] != ''):
            word_picked.add(item[0])

    file = open(DATA_PATH + 'frequecy_library_list.csv', 'w')
    for item in word_picked:
        file.write(item + '\n')
    return word_picked


# prepare training data
# special char is : . -
def get_data(text_file, label_file, label_is_tag):
    mysql = mo.Mysql(mo.USER, mo.PWD, mo.DB_NAME, mo.TABLE_NAME)
    result_num = mysql.query_each()
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
        tags = str(result[4]).split('#')
        tags.sort()
        tag = ' '.join(tags).lower().replace('\n', ' ').replace('\t', ' ')

        # decide write what kind of info into file
        text = ''
        if (dependecy != '' and (',' not in dependecy) and ('$' not in dependecy)):
            if (description != '' and get_length(description) > 2):
                text = description
            elif (readme != '' and get_length(readme) > 2):
                text = readme
            if (text != ''):
                if (label_is_tag and not tag == ''):
                    text_file.write(text + '\n')
                    label_file.write(tag + '\n')
                elif (not label_is_tag):
                    text_file.write(text + '\n')
                    label_file.write(dependecy + '\n')

    mysql.close_connection()


# split data into train, dev, test data
def train_test_split(library_set, code_all, tag_all, code_train, tag_train, code_dev, tag_dev, code_test, tag_test,
                     dev_percent, test_percent):
    # here you should know in linux wc-l's result is different to len(f.readlines())
    codes = code_all.read().split('\n')
    tags = tag_all.read().split('\n')
    print len(codes)
    print len(tags)
    dev_number = int(dev_percent * len(codes))
    test_number = int(test_percent * len(codes))
    for code, tag, index in zip(codes, tags, range(len(codes))):
        new_tag = []
        library = tag.split(' ')
        for l in library:
            if (l in library_set):
                new_tag.append(l)
        print str(len(new_tag))+'----------'+str(len(str(code).split(' ')))
        new_tag = ' '.join(new_tag)
        if (new_tag != ''):
            if (index < test_number):
                code_test.write(code + '\n')
                tag_test.write(new_tag + '\n')
            elif (index < test_number + dev_number):
                code_dev.write(code + '\n')
                tag_dev.write(new_tag + '\n')
            else:
                code_train.write(code + '\n')
                tag_train.write(new_tag + '\n')
        #print index


if __name__ == "__main__":
    handler = FileHandler(DATA_PATH)
    # code_all, tag_all = handler.get_all_file('text_all','label_all','a')
    # get_data(code_all, tag_all,True)
    # code_all.close()
    # tag_all.close()

    code_all, tag_all = handler.get_all_file('text_all', 'label_all', 'r')
    library_set = get_frequet_library(tag_all)
    code_all.close()
    tag_all.close()
    #
    # code_all, tag_all = handler.get_all_file('text_all', 'label_all', 'r')
    # code_train,tag_train = handler.get_train_file('giga-fren.release2.fixed.en','giga-fren.release2.fixed.fr')
    # code_dev,tag_dev = handler.get_dev_file('newstest2013.en','newstest2013.fr')
    # code_test,tag_test = handler.get_test_file('text.test','label.test')
    # train_test_split(library_set,code_all, tag_all,code_train,tag_train,code_dev,tag_dev,code_test,tag_test,0.1,0.2)
    # code_all.close()
    # tag_all.close()
    # code_train.close()
    # tag_train.close()
    # code_dev.close()
    # tag_dev.close()
    # code_test.close()
    # tag_test.close()
