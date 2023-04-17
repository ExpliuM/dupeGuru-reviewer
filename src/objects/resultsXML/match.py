#!/usr/bin/python3
'''match module'''


class Match():
    '''Match class'''

    def __init__(self, element):
        self.element = element
        self.first = element.attrib['first']
        self.second = element.attrib['second']
        self.percentage = element.attrib['percentage']

    def __str__(self,
                endOfObjectDelimiter='\n',
                memberDelimiter='\n\t',
                subMemberDelimiter='\n\t\t'):
        memberDelimiter += '\t'
        subMemberDelimiter += '\t\t'
        return "Match: attributes=" + self.element.attrib.__str__()
