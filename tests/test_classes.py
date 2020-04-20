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

    def test_get_data(self):
        data=self.table.get_data()
        self.assertEqual(self.table.data, data)

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

    def test_corona(self):
        self.corona.get_table()
        data_new = WorkWithCsvTable()
        data_new.read_table("google.csv")
        data=data_new.get_data()
        self.assertEqual(self.corona.table, data)

class TestsFacts(unittest.TestCase):

    def test_bad_request(self):
        with patch('team_4ever.classes.requests.get') as mock_get:
            mock_get.return_value.status_code = 0
            facts = Website('http://google.com').get_data()
        self.assertEqual(facts, None)

    def test_ok_request(self):
        with patch('team_4ever.classes.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = 'hello'
            data = Website('http://google.com').get_data()
        self.assertEqual(data, 'hello')


if __name__ == '__main__':
    unittest.main()
