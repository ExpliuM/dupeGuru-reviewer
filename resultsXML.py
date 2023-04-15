#!/usr/bin/python3

from group import Group;

import xml.etree.ElementTree as ElementTree


class ResultsXML():
    def __init__(self, resultsXMLFileFullPath):
        self.tree = ElementTree.parse(resultsXMLFileFullPath)

    def getTree(self):
        return self.tree

    def getGroups(self):
        return [Group(x) for x in self.tree.getroot()]

    def __str__(self):
        return ElementTree.tostring(self.tree.getroot(), encoding='utf8', method='xml')
