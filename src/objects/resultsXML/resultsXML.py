#!/usr/bin/python3
'''resultsXML module'''

import xml.etree.ElementTree as ElementTree

from src.objects.resultsXML.group import Group


class ResultsXML():
    '''resultsXML class'''

    def __init__(self, resultsXMLFileFullPath):
        self.tree = ElementTree.parse(resultsXMLFileFullPath)

    def getTree(self):
        '''getTree method'''
        return self.tree

    def getGroups(self):
        '''getGroups method'''
        return [Group(x) for x in self.tree.getroot()]

    def __str__(self):
        return ElementTree.tostring(self.tree.getroot(), encoding='utf8', method='xml')
