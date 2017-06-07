#!/usr/bin/python
# coding=utf-8
import re
import sys
import mistune

reload(sys)
sys.setdefaultencoding('utf-8')

MAX_STRING_LENGTH = 200


def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i) < 128)


def clean(text):
    try:
        if (text == '' or text == None):
            return ''
        text = remove_non_ascii_1(text)
        text = re.sub('&lt', '<', text)
        text = re.sub('&gt', '>', text)
        text = re.sub('<;', ' ', text)
        text = re.sub("<(.+?)/(.+?)>", ' ', text)
        text = re.sub("<(.+?)>", ' ', text)
        text = re.sub('\[',' ',text)
        text = re.sub(']',' ',text)
        text = re.sub('"', ' ', text)
        text = re.sub('!', ' ', text)
        text = re.sub('#', ' ', text)
        text = re.sub('{', ' ', text)
        text = re.sub('}', ' ', text)
        text = re.sub('\|', ' ', text)
        text = re.sub('\*', ' : ', text)
        text = re.sub('=', ' ', text)
        text = re.sub('\$', ' ', text)
        text = re.sub('"', ' ', text)
        text = re.sub('/','',text)
        text = re.sub('\(',' ',text)
        text = re.sub('\)', ' ', text)
        text = re.sub('<',' ',text)
        text = re.sub('>',' ',text)
        text = re.sub('\.',' ',text)
        text = re.sub('-', ' ', text)
        text = re.sub(':', ' : ', text)
        text = re.sub(' +', ' ', text)
        text = re.sub('\n+', '\n', text)
    except Exception, e:
        print e
        print 'ERROR OF clean'
    return text.strip()

def camel_case_split(text):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', text)
    texts = [m.group(0) for m in matches]
    texts = [t.lower() for t in texts]
    return ' '.join(texts)


def data_prepare_clean(text):
    text = clean(text)
    texts = text.split(' ')
    texts = [camel_case_split(t) for t in texts]
    return ' '.join(texts)


def base64_to_utf8(file):
    with open(file, 'r') as f:
        text = f.read()
        print text
        encoded = text.decode('base64')
        return encoded.encode('utf-8')

#get description from readme file
def extract_markdown(text):
    url = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.' \
          '[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\
          .[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})'
    text = re.sub(url, '', text)
    text = clean(text)
    xml = "<(.+?)/(.+?)>"
    text = re.sub(xml, '', text)
    text = text.replace(',', ' ')
    pattern = re.compile(r'\#+(.+?)\#+', flags=re.DOTALL)
    result = re.findall(pattern, text)
    if (len(result) > 10):
        return result[0].replace('\n', ' ')
    else:
        text = mistune.markdown(text)
        pattern = re.compile(r'<p(.+?)/p>+', flags=re.DOTALL)
        result = re.findall(pattern, text)
        if (len(result) != 0):
            return result[0].replace('\n', ' ')
        else:
            info = (text[:MAX_STRING_LENGTH] + ' ...') if len(text) > MAX_STRING_LENGTH else text
            return clean(info)


if __name__ == "__main__":
    a = '2011-01-26T19:01:12Z'
    b = '2010-12-6T20:01:12Z'
    print b > a
    #print camel_case_split('CamelCaseXYZ CamelCaseXYZ fr ')
    # print remove_non_ascii_1('sdwodesds~~~')
    # print clean('fs\n\n   ff ')
    # print base64_to_utf8('/home/yangqiao/1')
    # print extract_markdown(open('text.md', 'r').read())
