#!/usr/bin/python3
'''group module'''

from src.objects.resultsXML.file import File
from src.objects.resultsXML.match import Match

class Group():
    '''Group class'''

    def __init__(self, element):
        self.files = [File(element) for element in filter(
            lambda child: (child.tag == 'file'), element)]

        self.matches = [Match(element) for element in filter(
            lambda child: (child.tag == 'match'), element)]

    def getFiles(self):
        '''getFiles method'''
        return self.files

    def getPaths(self):
        '''getPaths method'''
        return [f.getPath() for f in self.files]

    def getMatches(self):
        '''getMatches method'''
        return self.matches

    def __str__(self, endOfObjectDelimiter='\n', memberDelimiter='\n\t'):
        subMemberDelimiter = memberDelimiter+'\t'
        filesString = subMemberDelimiter + \
            ''.join(
                [x.__str__(endOfObjectDelimiter, memberDelimiter=subMemberDelimiter) +
                 subMemberDelimiter for x in self.files])
        matchesString = subMemberDelimiter+''.join(
            [x.__str__(endOfObjectDelimiter, memberDelimiter=subMemberDelimiter) +
             subMemberDelimiter for x in self.matches])
        return "Group:" + memberDelimiter + \
            "Files=" + filesString + memberDelimiter + \
            "Matches=" + matchesString + endOfObjectDelimiter
