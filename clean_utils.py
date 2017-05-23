#!/usr/bin/python
#coding=utf-8
import re
import sys
import base64

reload(sys)
sys.setdefaultencoding('utf-8')

def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i)<128)

def clean(text):
    text = re.sub(' +', ' ',text)
    text = re.sub('\n+','\n',text)

    return text


def base64_to_utf8(file):
    with open(file,'r') as f:
        text = f.read()
        print text
        encoded = text.decode('base64')
        return encoded.encode('utf-8')



print remove_non_ascii_1('sdwodesds~~~')
print clean('fs\n\n   ff ')
print base64_to_utf8('/home/yangqiao/1')