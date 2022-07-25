#!/usr/bin/python3

import defines
import resultsXML
import unittest


class TestResultsXML(unittest.TestCase):
    def test_init(self):
        resultsXMLObj = resultsXML.ResultsXML(defines.RESULTS_FULL_FILE_PATH)

        object_string = ''.join([str(x) for x in resultsXMLObj.getGroups()])
        print(object_string)


if __name__ == '__main__':
    unittest.main()
