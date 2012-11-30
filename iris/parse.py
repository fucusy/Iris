#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse
#
# parse module turn a wikipedia xml file into the database we need

import sys
import gc
import re

from lxml import etree
import jieba

from .db import *
from . import stopwords,log

# tag_prefix if the namespace of the page info in xml file
# if you download the wikipedia dumped xml file yourself, 
# you may need to change the tag_prefix
tag_prefix = "{http://www.mediawiki.org/xml/export-0.7/}"

#-------Utils--------------
trim_with_prefix = lambda s,pre: s[len(pre):]
trim = lambda s: trim_with_prefix(s,tag_prefix)
text_len = lambda s: len(s) if isinstance(s,unicode) else 0
#--------------------------



def parse_xml(xml_file="/Users/bank/Downloads/wiki.xml",max_count=100000):
    """
    parse_xml takes a xml file and use it create two tables we need.
    """
    try:
        con = None
        count = 0
        con = db_open()
        for event, element in etree.iterparse(xml_file,tag=tag_prefix+'page'):
            # call parse_data to get id,title,and text
            docid,title,text = parse_data(element)
            word_list = get_words_from_text(text)
            if word_list and count < max_count:
                for w in word_list:
                    if is_legal(w):
                        insert_inverted_index(con,w.lower(),docid)
            links = get_link_from_text(text)
            insert_doc_info(con,docid,title,links)
            count += 1
            del element
            print "Page:",count
            if (count%100000) == 0:
                # if your ram is not large, you need to collect the garbages to avoid frequently swap
                gc.collect()
    except KeyboardInterrupt:
        raise 
    finally:
        db_close(con)


def parse_data(element):
    """
    get the id, title and text information from a node in the xml tree.
    """
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

def get_words_from_text(text):
    """
    Return the segmentation(tokens) of the text.
    Using jieba library to split the text
    """
    if text:
        seg = jieba.cut(text,cut_all=True)
        return seg
    return None

def get_link_from_text(text):
    """
    Use regex to get all wiki page links one page contains
    A link is looks like [[页面]]
    """
    link_pattern = ur'\[\[(.+?)\]\]'
    p = re.compile(link_pattern)
    l = []
    if text:
        l = p.findall(text)
    return l


#-------Useless pages------
white_pattern = '\s+'
pound_pattern = '#.*'
number_pattern = '\d+'

wre = re.compile(white_pattern)
pre = re.compile(pound_pattern)
nre = re.compile(number_pattern)
#------------------------------

def is_legal(w):
    """
    tell if a word is helpful.
    """
    if wre.match(w) or pre.match(w) or nre.match(w) or ere.match(w) or len(w) < 2 or w in stopwords:
        return False
    return True;



