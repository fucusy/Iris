#!/usr/bin/env python
# -*- coding: utf-8 -*-

# create_database
# 
# If you running the script on new machine, you need create the database and tables first.
# Notice: the dataset is really huge (a xml file over 5Gb), if you just wanna test it, input a small max_count
#         if you need to evaluate, please contact the author for the pre-generated database.

import sys
import MySQLdb as db

from iris.parse import *

def main(usesrname,password,xml_file,max_count=100000):
    try:
        print "--- Start create database and tables ---"
        con = db.connect(host="127.0.0.1",user=username,passwd=password)
        cur = con.cursor()

        cur.execute("CREATE DATABASE wiki")
        cur.execute("USE wiki")
        print "Table: docs"
        cur.execute("""CREATE TABLE `docs` (
                       `id` int(11) unsigned NOT NULL,
                       `title` varchar(80) CHARACTER SET utf8mb4 DEFAULT NULL,
                       `links` text CHARACTER SET utf8mb4,
                        PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;""")
        print "Table: inverted_index"
        cur.execute("""CREATE TABLE `inverted_index` (
                       `word` varchar(20) NOT NULL,
                       `id` int(11) unsigned NOT NULL,
                       `freq` int(11) unsigned NOT NULL,
                       PRIMARY KEY (`word`,`id`)
                       ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;""")

        con.close()

        print "--- Start import data from xml ---"
        parse_xml(xml_file,max_count)
    except db.Error,e:
        raise


if __name__ == '__main__':
    print "You must install MySQL(>5.5) on your machine"
    username = raw_input("Please input mysql username:")
    password = raw_input("Please input mysql password:")
    xml_file = raw_input("Please input xml file path:")
    max_count = raw_input("How many pages you want to import:")
    main(username,password,xml_file,int(max_count))
