#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re

print "--- Preprocessingi and building ---"
from iris.query import *
print "-----------------------------------"


def search(query,n=10):
    title_result = search_title(query)
    if title_result:
        print 0,title_result[1]
    result = rank(handle_query(query))
    if not result:
        print "Nothing..."
        return

    if n > len(result):
        n = len(result)

    for i,item in enumerate(result[0:n]):
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
