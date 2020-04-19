import unittest
from unittest import mock
from unittest.mock import patch

from classes import WorkWithCsvTable,  WorkWithCoronaData, Website

class TestsWorkWithCsvTable(unittest.TestCase):
    def setUp(self):
        self.table = WorkWithCsvTable()

    def tearDown(self):
        self.table.data=[]

    def test_write_no_table(self):
        self.table.data=[]
        mock_open_handler = mock.mock_open()
        with patch('classes.open', mock_open_handler):
            self.table.write_table("history.txt")

    def test_write_table(self):
        self.table.data=[{'Country_Region': 'test1_coutry', 'Province_State': 'test_state'},
                         {'Country_Region': 'test2_coutry', 'Province_State': 'test_state'}]
        mock_open_handler = mock.mock_open()
        with patch('classes.open', mock_open_handler):
            self.table.write_table("history,txt")



    def test_read_table(self):
        self.table.read_table("google0.csv")
        self.assertEqual(self.table.data, [{'Active': '9','Confirmed': '9','Country_Region': 'US','Deaths': '0','Province_State': 'South Carolina','Recovered': '0'}])

    def test_read_no_table(self):
        self.table.read_table("google1.csv")
        self.assertEqual(self.table.data, [])

class TestsWorkWithCorornaData(unittest.TestCase):
    def setUp(self):
        self.corona= WorkWithCoronaData({}, [0] * 1000, [], [], {}, 0)

    def tearDown(self):
        self.prov = {}
        self.count = []
        self.data1 = []
        self.table = []
        self.now = []
        self.day = 0


if __name__ == '__main__':
    unittest.main()
