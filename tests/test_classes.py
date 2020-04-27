import unittest
from unittest import mock
from unittest.mock import patch
from pymongo import MongoClient

from team_4ever.classes import WorkWithCsvTable,  WorkWithCoronaData, Website, WriteDb

with open("data_for_tests\\google0.csv", 'w') as doc:
    doc.write('Province_State,Country_Region,Confirmed,Deaths,Recovered,Active\nSouth Carolina,US,9,0,0,9')
with open("data_for_tests\\google1.csv", 'w') as doc:
    doc.write('')

table = [{'Province_State': 'South Carolina', 'Country_Region': 'US', 'Confirmed': '9', 'Deaths': '0', 'Recovered': '0',
          'Active': '9'}]


class TestsWorkWithCsvTable(unittest.TestCase):
    def setUp(self):
        self.table = WorkWithCsvTable(data=[])

    def tearDown(self):
        self.table.data = []

    def test_write_no_table(self):
        self.table.data = []
        mock_open_handler = mock.mock_open()
        with patch('classes.open', mock_open_handler):
            self.table.write_table("history.txt")

    def test_write_table(self):
        self.table.data = [{'Country_Region': 'test1_country', 'Province_State': 'test_state'},
                           {'Country_Region': 'test2_country', 'Province_State': 'test_state'}]
        mock_open_handler = mock.mock_open()
        with patch('classes.open', mock_open_handler):
            self.table.write_table("history,txt")

    def test_get_data(self):
        data = self.table.get_data()
        self.assertEqual(self.table.data, data)

    def test_read_table(self):
        self.table.read_table("data_for_tests\\google0.csv")
        self.assertEqual(self.table.data, [{'Active': '9', 'Confirmed': '9', 'Country_Region': 'US', 'Deaths': '0',
                                            'Province_State': 'South Carolina', 'Recovered': '0'}])

    def test_read_no_table(self):
        self.table.read_table("data_for_tests\\google1.csv")
        self.assertEqual(self.table.data, [])


class TestsWorkWithCoronaData(unittest.TestCase):
    def setUp(self):
        self.corona = WorkWithCoronaData([], [0] * 1000, [], [], {}, 0)

    def tearDown(self):
        self.prov = []
        self.count = []
        self.data1 = []
        self.table = []
        self.now = []
        self.day = 0

    def test_corona(self):
        self.corona.get_table()
        data_new = WorkWithCsvTable(data=[])
        data_new.read_table("data_for_tests\\google2_0.csv")
        data = data_new.get_data()
        self.assertEqual(self.corona.table, data)


class TestsFacts(unittest.TestCase):

    def test_bad_request(self):
        with patch('classes.requests.get') as mock_get:
            mock_get.return_value.status_code = 0
            facts = Website('http://google.com').get_data()
        self.assertEqual(facts, None)

    def test_ok_request(self):
        with patch('classes.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = 'hello'
            data = Website('http://google.com').get_data()
        self.assertEqual(data, 'hello')


class TestsDB(unittest.TestCase):

    def setUp(self):
        self.db = WriteDb()
        self.db.data = []
        self.db.file = ''

    def test_write_db(self):
        client = MongoClient()
        db_example = client['12']
        self.db.file = 'data_for_tests\\google0.csv'
        self.db.write_db('1', '12')
        self.assertEqual(db_example['1'].find_one({'Province_State': 'South Carolina'}, {'_id': 0}),
                         {'Province_State': 'South Carolina', 'Country_Region': 'US', 'Confirmed': 9, 'Deaths': 0,
                          'Recovered': 0, 'Active': 9})

    def test_bad_find_doc(self):
        self.assertEqual(self.db.find_doc('2', '12'), 0)

    def test_ok_write_db(self):
        self.assertNotEqual(self.db.find_doc('1', '12'), 0)


if __name__ == '__main__':
    unittest.main()
