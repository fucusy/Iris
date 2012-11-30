#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Query
#
# query module handle the work aroung queries
# it includs search a word/title/doc, rank the result, remove irrelevant pages

import re
import math

import jieba

from . import stopwords
from .db import *

#--------- Special Wikipedia pages pattern -----------
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
#-----------------------------------------------------

def handle_query(query):
    "Input: a query. Output: (id,title) list"
    try:
        result = {}
        con = None
        con = db_open()
        # Split the chinese query into words/phrases
        query_seg = jieba.cut(query,cut_all=False)
        # eliminate the stopwords and single charactor word
        querys = [w for w in query_seg if w not in stopwords and len(w) > 1]
        for q in querys:
            l = db_query(con,q)
            result[q] = l
        # return the rank of the results
        return rank(result)
    except db.Error,e:
        raise
    finally:
        db_close(con)

def search_title(query):
    "Search if query is somepage's title"
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
    total_doc_numbers = db_get_doc_number(con)

    for w in result: #for every word
        total_freq = 0.0
        df = len(result[w])
        print "Word:",w,"Document length:",df
        for t in result[w]:
            #t:(id,freq) of word w
            total_freq += t[1] # calculate the total_freq
            if t not in docs:
                docs[t] = {}
                docs[t]["id"] = t[0]
                docs[t]["title"] = db_search_title(con,t[0])
                docs[t]["freq"] = 0.0
                docs[t]["count"] = 0
    
        for t in result[w]:
            # the final freq will the sum of uniformed tf-idf of each term/word
            docs[t]["freq"] += float(t[1]*len(w))/total_freq * math.log(float(total_doc_numbers)/df,2)
            docs[t]["count"] += 1

    # then we eliminate the un-helping pages
    l = [docs[d] for d in docs if is_useful(docs[d]["title"])]
    db_close(con)
    # we sort the result using rank_score() function
    l.sort(key=lambda x: rank_score(x), reverse=True)
    return l


def rank_score(x):
    """
    Caclute the score of each doc.
    For a more relevant doc, intuitively we need it to cover
    more words in query. Thus furthur than just sum the frequency, 
    we multiply it by the the square of the number that words it contains.
    It turns out good result.
    """
    return x["freq"]*(x["count"]**2)

def is_useful(t):
    """To check if a page is a useful one"""
    if wre.match(t)  or \
       wtre.match(t) or \
       tre.match(t)  or \
       hre.match(t)  or \
       ure.match(t)  or \
       utre.match(t) or \
       tempre.match(t):
        return False
    return True

       

             
