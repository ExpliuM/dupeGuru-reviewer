#!/usr/bin/python3

from defines import DEFAULT_RESULTS_FULL_FILE_PATH

import resultsXML
import unittest


class TestResultsXML(unittest.TestCase):
    def test_init(self):
        resultsXMLObj = resultsXML.ResultsXML(DEFAULT_RESULTS_FULL_FILE_PATH)

        object_string = ''.join([str(x) for x in resultsXMLObj.getGroups()])
        print(object_string)


if __name__ == '__main__':
    unittest.main()

# TODO: To implement tests