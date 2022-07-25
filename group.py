#!/usr/bin/python3

import file
import match


class Group():
    def __init__(self, element):
        self.files = [file.File(element) for element in filter(
            lambda child: (child.tag == 'file'), element)]

        self.matches = [match.Match(element) for element in filter(
            lambda child: (child.tag == 'match'), element)]

    def getFiles(self):
        return self.files

    def getPaths(self):
        return [f.getPath() for f in self.files]

    def getMatches(self):
        return self.files

    def __str__(self, endOfObjectDelimiter='\n', memberDelimiter='\n\t'):
        subMemberDelimiter = memberDelimiter+'\t'
        filesString = subMemberDelimiter + \
            ''.join([x.__str__(endOfObjectDelimiter, memberDelimiter=subMemberDelimiter) +
                    subMemberDelimiter for x in self.files])
        matchesString = subMemberDelimiter+''.join(
            [x.__str__(endOfObjectDelimiter, memberDelimiter=subMemberDelimiter)+subMemberDelimiter for x in self.matches])
        return "Group:" + memberDelimiter + "Files=" + filesString + memberDelimiter + "Matches=" + matchesString + endOfObjectDelimiter
