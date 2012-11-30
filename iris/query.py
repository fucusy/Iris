#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from . import stopwords
from .db import *
import jieba

wiki_pattern = "^Wikipedia:.+"
wikitalk_pattern = "^Wikipedia talk:.+"
talk_pattern = "^Talk:.+"
help_pattern = "^Help:.+"
user_pattern = "^User:.+"
usertalk_pattern = "^User talk:.+"
template_pattern = "^Template:.+"

wre = re.compile(wiki_pattern)
wtre = re.compile(wikitalk_pattern)
tre = re.compile(talk_pattern)
hre = re.compile(help_pattern)
ure = re.compile(user_pattern)
utre = re.compile(usertalk_pattern)
tempre = re.compile(template_pattern)

def handle_query(query):
    "Input: a query. Output: (id,title) list"
    try:
        result = {}
        con = None
        con = db_open()
        query_seg = jieba.cut(query,cut_all=True)
        querys = [w for w in query_seg if w not in stopwords and len(w) > 1]
        for q in querys:
            l = db_query(con,q)
            result[q] = l
        return result
    except db.Error,e:
        raise
    finally:
        db_close(con)

def search_title(query):
    try:
        con = None
        con = db_open()
        l = db_search(con,query)
        return l
    except db.Error,e:
        raise
    finally:
        db_close(con)

def rank(result):
    """Input: a dict, each item is a list of tuples.
       Output: A list of titles with ranks
    """
    con = db_open()
    docs = {}

    for w in result: #for every word
        total_freq = 0.0
        for t in result[w]:
            total_freq += t[1] 
            if t not in docs:
                docs[t] = {}
                docs[t]["id"] = t[0]
                docs[t]["title"] = get_title(con,t[0])
                docs[t]["freq"] = 0.0
                docs[t]["count"] = 0
    
        for t in result[w]:
            docs[t]["freq"] += float(t[1]*len(w))/total_freq
            docs[t]["count"] += 1
    
        l = [docs[d] for d in docs if is_useful(docs[d]["title"])]
        db_close(con)
        l.sort(key=lambda x: rank_score(x), reverse=True)
        return l


def rank_score(x):
    return x["freq"]*x["count"]

def is_useful(t):
    if wre.match(t)  or \
       wtre.match(t) or \
       tre.match(t)  or \
       hre.match(t)  or \
       ure.match(t)  or \
       utre.match(t) or \
       tempre.match(t):
        return False
    return True

# query = "最好的文本编辑器"
# l = rank(handle_query(query))
# for i in l[0:10]:
#     print i["title"],i["freq"],i["count"]
       

             
