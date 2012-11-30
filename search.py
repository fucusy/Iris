#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Search
#
# In this cripte we provide a command line interface
# User input a query and expected result number, the program will
# return a list of result pages based on the relevance.

import sys

print "--- Preprocessing and building ---"
from iris.query import *
print "-----------------------------------"


def search(query,n=10):
    "Search: the main api"
    # If the query itself is the page title, we return it first
    title_result = search_title(query)
    if title_result:
        print 0,title_result[1]
    # calling query.handle_query to deal with the words
    result = handle_query(query)
    if not result:
        print "Nothing..."
        return

    if n > len(result):
        n = len(result)

    for i,item in enumerate(result[0:n]):
        # We print title here
        # One can print freq(score) and count also
        print i+1,item["title"]
    


if __name__ == '__main__':
    print "** Input Chinese to search, quit to quit **"
    n = 10
    input_n = raw_input("List length(default 10):")
    if re.match("^\d.+$",input_n):
        n = int(input_n)
    while True:
        query = raw_input("Input query:")
        if query == "quit":
            print "Bye"
            sys.exit()
        print "-----"+query+"-----"
        search(query,n)
        print 
