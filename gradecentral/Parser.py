#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:21:04 2019

@author: JustinChen
"""
from bs4 import BeautifulSoup
import urllib.request
import re

#%%
def getClasses(searchInput):
    """
    Returns a list of class match objects from the classes.berkeley.edu website
    Uses the user's input search term, where the first part is the department
    (Ex. Math, Compsci, etc.) followed by course number separated by a space.
    """
    #TODO
    
    #soup = BeautifulSoup(html_doc, 'html.parser')
    
    #return BeautifulSoup(html_doc, 'html.parser')
    
    return getResults(htmlString(searchInput))

class Class:
    json = {}
    priority = 0
    
    def __init__(self, info, priority):
        self.json, self.priority = info, priority
    
#%%
def htmlString(search):
    """ 
    Uses user input to search for in classes.berkeley.edu and returns the
    string representation of HTML code
    """
    userInput = search.split(' ')
    department, num = userInput[0], userInput[1]
    site = ('https://classes.berkeley.edu/search/class/' + department + '%2520' 
            + num + '?f%5B0%5D=im_field_term_name%3A851&retain-filters=1')
    
    #Opens website and converts to html string
    fp = urllib.request.urlopen(site)
    mybytes = fp.read()
    html_doc = mybytes.decode("utf8")
    fp.close()
    
    return html_doc

def getResults(html):
    """
    Returns a list of class objects including dictionaries of relevant info:
    
    id: class ID
    name: class display name
    section: class section number
    title: full official name of class
    
    and a priority of search result order
    """
    matches = re.findall("data-json='.+}\'", html)
    classes, p, i = [], 1, 0
    nodes = [eval(x) for x in getNodeInfo(html)]
    for match in matches[:10]:
        match, json = match[11:], "{"
        lst = match.split(',')
        name, section = getName(lst)
        json = eval(json + ','.join([getID(lst), name, section, getTitle(lst)]) + '}')
        json.update(nodes[i])
        classes.append(Class(json, p))
        p += 1
        i += 1
    return classes
    
def getNodeInfo(html):
    """
    Returns a list of node info json dicts represented as strings since they 
    are not covered by regex matching.
    """
    cleaned, new = [], html
    for _ in range(10):
        try:
            index = new.index('data-node')
        except ValueError:
            cleaned.append("{'error':'no-data'}")
            return cleaned
        new = new[index:]
        unclean = new[11:new.index("}'") + 1]
        cleaned.append(cleanNodeInfo(unclean))
        #arbitrary large number
        new = new[index + 2000:]
    return cleaned
#%%        
def cleanNodeInfo(unclean):
    """ 
    Returns a cleaned version of the node info string.
    Originally with \n and space characters before each key-value pair, 
    this function cleans it so it looks like a dict but in string form.
    """
    lst, i = unclean.split(','), 0
    splitInd, split = 0, False
    for item in lst:
        if item[0] == '\n':
            lst[i] = item[15:]
        if lst[i][16:27] == 'nodeUpdated':
            lst[i] = lst[i] + lst[i + 1]
            split, splitInd = True, i + 1
        i += 1
    if split:
        lst = lst[:splitInd] + lst[splitInd + 1:]
    return ','.join(lst)

def getID(lst):
    """ 
    Takes in a list of all the individual components of the string html json
    and returns the class ID number (as a string)
    """
    for item in lst:
        if 'id' in item.split('"'):
            index = item.index(':')
            return '"id":' + str(item[index + 1:]) 
        
def getName(lst):
    """ 
    Takes in a list of all the individual components of the string html json
    and returns the Name & Section # (as a string)
    """
    for item in lst:
        if 'displayName' in item.split('"'):
            full = item[item.index(':') + 1:]
            parts = full.split(' ')
            name = ' '.join(parts[2:4])
            section = parts[4]
            return '"name":' + '"' + name + '"', '"section":' + '"' + section + '"'

def getTitle(lst):
    """ 
    Takes in a list of all the individual components of the string html json
    and returns the official full class name (as a string)
    """
    for item in lst:
        if 'title' in item.split('"'):
            index = item.index(':')
            return '"title":' + item[index + 1:]
    