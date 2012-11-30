#!/usr/bin/env python
# -*- coding: utf-8 -*-

# db
#
# db.py contains all database-involved operations
# It can be viewed as the database api of the project

import sys
# We are using mysql as our database server program
import MySQLdb as db

username = 'root'
password = ''


def db_open(ip='127.0.0.1',user=username,passwd=password,database='wiki'):
    "Connect a database then return the connection object"
    con = None
    try:
        con = db.connect(ip,user,passwd,database,charset='utf8')
    except db.Error:
        raise db.Error
    return con

def db_close(con):
    "Close a connection"
    if con:
        con.close()

def db_query(con,q):
    "Inverted Index search. Given a word, return all docs that contains it"
    search_query = """SELECT id,freq FROM inverted_index WHERE word = %s"""
    cur = con.cursor()
    cur.execute(search_query,(q))
    result = list(cur.fetchall())
    return result

def db_search(con,title):
    "Plain search. Given a title, return its id"
    search_query = """SELECT id,title FROM docs WHERE title = %s"""
    cur = con.cursor()
    cur.execute(search_query,(title))
    result = cur.fetchone()
    if result and result[0]:
        return result
    return None

def db_get_doc_number(con,test=False):
    "return current number of docs"
    if test:
        return 100000
    else:
        search_query = "SELECT COUNT(*) FROM docs"
        cur = con.cursor()
        cur.execute(search_query)
        result = cur.fetchone()
        if result and result[0]:
            return int(result[0])
        return 0

def db_search_title(con,docid):
    "Given a doc_id, return the corresponding title"
    search_query = """SELECT title FROM docs WHERE id = %s"""
    cur = con.cursor()
    cur.execute(search_query,(docid))
    data = cur.fetchone()
    if data and data[0]:
        return data[0]
    return None

def insert_doc_info(con,docid,title,links):
    "Insert a record in docs table"
    con.ping()
    cur = con.cursor()
    link_text = "|".join(links)
    insert_query = """INSERT IGNORE INTO 
                      docs (id,title,links) 
                      VALUES (%s,%s,%s)"""
    data = cur.execute(insert_query,(docid,title,link_text))
    con.commit()
    return data
    
def insert_inverted_index(con,word,docid):
    "Insert a record in inverted index"
    insert_query = """INSERT IGNORE INTO inverted_index (word,id,freq) VALUES (%s,%s,%s)"""
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

#not_working
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
                
    



        

        
        


