#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import gc
import re
# reload(sys) 
# sys.setdefaultencoding('utf-8')

from lxml import etree
import jieba

from .db import *
from . import stopwords,log

xml_file = "/Users/bank/Downloads/wiki.xml"
tag_prefix = "{http://www.mediawiki.org/xml/export-0.7/}"

trim_with_prefix = lambda s,pre: s[len(pre):]
trim = lambda s: trim_with_prefix(s,tag_prefix)
text_len = lambda s: len(s) if isinstance(s,unicode) else 0

white_pattern = '\s+'
pound_pattern = '#.*'
number_pattern = '\d+'
# english_pattern = '[a-zA-Z]+'
wre = re.compile(white_pattern)
pre = re.compile(pound_pattern)
nre = re.compile(number_pattern)
# ere = re.compile(english_pattern)

def parse_xml(xml_file):
    try:
        con = None
        count = 0
        con = db_open()
        for event, element in etree.iterparse(xml_file,tag=tag_prefix+'page'):
            docid,title,text = parse_data(element)
            word_list = get_words_from_text(text)
            if word_list and count > 18554:
                for w in word_list:
                    if is_legal(w):
                        insert_inverted_index(con,w.lower(),docid)
            # links = get_link_from_text(text)
            # insert_doc_info(con,docid,title,links)
            # insert_link(con,docid,links)
            count += 1
            del element # for extra insurance
            print count
            if (count%100000) == 0:
                gc.collect()
    except KeyboardInterrupt:
        raise 
    finally:
        db_close(con)


def parse_data(element):
    title = docid = text = None
    for child in element.iterchildren():
        if trim(child.tag) == 'title':
            title = child.text
        elif trim(child.tag) == 'id':
            docid  = int(child.text)
        elif trim(child.tag) == 'revision':
            for grandchild in child:
                if trim(grandchild.tag) == 'text':
                    text = grandchild.text
    del element
    return docid,title,text

def encode(content):
    if isinstance(content,unicode):
        return content
    return nt


def get_words_from_text(text):
    if text:
        seg = jieba.cut(text,cut_all=True)
        return seg
    return None

def get_link_from_text(text):
    link_pattern = ur'\[\[(.+?)\]\]'
    p = re.compile(link_pattern)
    l = []
    if text:
        l = p.findall(text)
    return l


def is_legal(w):
    if wre.match(w) or pre.match(w) or nre.match(w) or ere.match(w) or len(w) < 2 or w in stopwords:
        return False
    return True;



# con = db_open()
# insert_link(con,991,["中华人民共和国","中华人民共和国"])
# db_close(con)

try:
    parse_xml(xml_file)
except KeyboardInterrupt:
    sys.exit()

# for i in get_link_from_text(test_text):
#     print i

