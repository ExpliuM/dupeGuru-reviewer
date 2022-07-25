#!/usr/bin/python3

import group
import xml.etree.ElementTree as ET


class ResultsXML():
    def __init__(self, resultsXMLFileFullPath):
        self.tree = ET.parse(resultsXMLFileFullPath)

    def getTree(self):
        return self.tree

    def getGroups(self):
        groups = [group.Group(x) for x in self.tree.getroot()]
        return groups

    def __str__(self):
        return ET.tostring(self.tree.getroot(), encoding='utf8', method='xml')
