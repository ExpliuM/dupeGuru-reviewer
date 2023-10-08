#!/usr/bin/python3

'''test module'''

import unittest
import logging

from src.defines import DEFAULT_RESULTS_FULL_FILE_PATH
from src.objects.resultsXML import resultsXML


class TestResultsXML(unittest.TestCase):
    '''TestResultsXML class'''

    def test_init(self):  # pylint: disable=invalid-name
        '''test_init method'''
        resultsXMLObj = resultsXML.ResultsXML(DEFAULT_RESULTS_FULL_FILE_PATH)

        objectString = ''.join([str(x) for x in resultsXMLObj.getGroups()])
        logging.debug(objectString)


if __name__ == '__main__':
    unittest.main()

# TODO: To implement tests
