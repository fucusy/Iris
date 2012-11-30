#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as db
import sys

link_table = "link"

def db_open():
    con = None
    try:
        con = db.connect('127.0.0.1','root','bankisme','wiki',charset='utf8')
    except db.Error:
        raise db.Error
    return con

def db_close(con):
    if con:
        con.close()

def db_query(con,q):
    search_query = """SELECT id,freq FROM inverted_index WHERE word = %s"""
    cur = con.cursor()
    cur.execute(search_query,(q))
    result = list(cur.fetchall())
    return result

def db_search(con,title):
    search_query = """SELECT id,title FROM docs WHERE title = %s"""
    cur = con.cursor()
    cur.execute(search_query,(title))
    result = cur.fetchone()
    if result and result[0]:
        return result
    return None


def get_title(con,docid):
    search_query = """SELECT title FROM docs WHERE id = %s"""
    cur = con.cursor()
    cur.execute(search_query,(docid))
    data = cur.fetchone()
    if data and data[0]:
        return data[0]
    return None

def insert_doc_info(con,docid,title,links):
    con.ping()
    cur = con.cursor()
    link_text = "|".join(links)
    insert_query = """INSERT IGNORE INTO 
                      docs (id,title,links) 
                      VALUES (%s,%s,%s)"""
    data = cur.execute(insert_query,(docid,title,link_text))
    con.commit()
    return data
    

def insert_link(con,docid,links):
    insert_query = """INSERT IGNORE INTO
                      links (from_id,to_id,freq)
                      values (%s,%s,%s)"""
    select_query = """SELECT id FROM docs WHERE title = %s"""
    update_query = """UPDATE links SET freq = freq + 1 WHERE from_id = %s AND to_id = %s"""
    cur = con.cursor()
    for title in links:
        cur.execute(select_query,(title))
        result = cur.fetchone()
        if result and result[0]:
            data = cur.execute(insert_query,(docid,result[0],1))
            con.commit()
            if data == 0:
                cur.execute(update_query,(docid,result[0]))
                con.commit()
                
    
def insert_inverted_index(con,word,docid):

    insert_query = """INSERT IGNORE INTO inverted_index (word,id,freq) VALUES (%s,%s,%s)"""
    # insert_query = """INSERT IGNORE INTO docs (id,title,links) VALUES (%s,%s,%s)"""

    update_query = """UPDATE inverted_index SET freq = freq + 1 WHERE word = %s AND id = %s"""
    cur = con.cursor()
    try:
        result = cur.execute(insert_query,(word,docid,1))
    except db.Error,e:
        print word,docid
        raise
    if result == 0: #exists
        cur.execute(update_query,(word,docid))
    con.commit()


        

        
        


