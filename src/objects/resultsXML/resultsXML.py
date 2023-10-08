#!/usr/bin/python3
'''resultsXML module'''

import os
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

    def getFilteredGroups(self):
        '''getGroups method'''
        groups = self.getGroups()

        return list(filter(self.filterGroupsWithHeicFiles, groups))

    def filterGroupsWithHeicFiles(self, group: Group):
        '''filterGroupsWithHeicFiles method'''
        paths = group.getPaths()

        _, fileExtension = os.path.splitext(paths[0])
        if fileExtension == ".heic":
            return False
        return True

    def getIndexOfFirstGroupWithMoreThanOneExistingFile(self):
        '''getGroups method'''
        groups = self.getFilteredGroups()
        for index, group in enumerate(groups):
            paths = group.getPaths()
            existingFiles = 0
            for path in paths:
                if os.path.exists(path):
                    existingFiles += 1
            if existingFiles > 1:
                return index

        return 0

    def __str__(self):
        return ElementTree.tostring(self.tree.getroot(), encoding='utf8', method='xml')
