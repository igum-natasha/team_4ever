import unittest
from unittest import mock
from unittest.mock import patch

from chat_bot_template1 import write_history, analise, write_facts, corona_write, corona_dynamics_write,\
    corona_russia_write, history
from classes import WorkWithCoronaData


@analise
def simple_action(update):
    return None


new_array = []
new_array1 = []
new_array2 = []
count = [1]


class TestsLogs(unittest.TestCase):
    def setUp(self):
        self.update = mock.MagicMock()

    def tearDown(self):
        global array
        array = []

    @patch('chat_bot_template1.array', new_array2)
    def test_log_action(self):
        self.update.message.text = 'hi'
        self.update.effective_user.first_name = 'Miki'
        simple_action(self.update)
        self.assertEqual(new_array2, [{'user': 'Miki', 'function': 'simple_action', 'message': 'hi'}])

    def test_no_message(self):
        self.update = mock.MagicMock(spec=['effective_user'])
        simple_action(self.update)
        self.assertEqual(array, [])

    def test_no_user(self):
        self.update = mock.MagicMock(spec=['message'])
        simple_action(self.update)
        self.assertEqual(array, [])

    def test_none_update(self):
        self.update = None
        simple_action(self.update)
        self.assertEqual(array, [])


class TestsHistory(unittest.TestCase):

    def setUp(self):
        self.update = mock.MagicMock()

    def tearDown(self):
        global array
        array = []

    def test_no_history(self):
        mock_open_handler = mock.mock_open()
        with patch('chat_bot_template1.open', mock_open_handler):
            reply_text = write_history(self.update, [])
        self.assertEqual(reply_text, [])

    @patch('chat_bot_template1.array', new_array1)
    def test_history(self):
        new_array1.append({'user': '1',
                           'function': 'func1',
                           'message': 'hello',
                           })
        mock_open_handler = mock.mock_open()
        with patch('chat_bot_template1.open', mock_open_handler):
            reply_text = write_history(self.update, new_array1)

        self.assertEqual(reply_text, ['Action 1:', 'user : 1', 'function : func1', 'message : hello'])

    @patch('chat_bot_template1.array', new_array)
    def test_history_no_user(self):
        self.update.effective_user.first_name = None
        mock_open_handler = mock.mock_open()
        with patch('chat_bot_template1.open', mock_open_handler):
            reply_text = write_history(self.update, new_array)
        self.assertEqual(reply_text, [])


class TestsWriteFacts(unittest.TestCase):
    def setUp(self):
        self.update = mock.MagicMock()

    def test_bad_url(self):
        web = write_facts(self.update, 'http://hi.com')
        self.assertEqual(web, '')

    def test_ok_url(self):
        web = write_facts(self.update, 'https://cat-fact.herokuapp.com/facts')
        self.assertNotEqual(web, "")


class TestWriteCorona(unittest.TestCase):
    def setUp(self):
        self.update = mock.MagicMock()
        self.provinces = mock.MagicMock()

    def test_5_lines_write(self):
        write_database = mock.MagicMock()
        with patch('chat_bot_template1.write_database', write_database):
            answer = corona_write(self.update)
        self.assertEqual(answer.count('\n'), 5)

    def test_ok_write(self):
        write_database = mock.MagicMock()
        with patch('chat_bot_template1.write_database', write_database):
            answer = corona_write(self.update)
        self.assertNotEqual(answer, "")


class TestWriteCoronaDynamic(unittest.TestCase):
    def setUp(self):
        self.update = mock.MagicMock()
        self.corona = WorkWithCoronaData([], [0]*1000, [], [], {}, 1)
        self.corona1 = WorkWithCoronaData([], [0]*1000, [], [], {}, 0)

    def test_ok_write(self):
        write_database = mock.MagicMock()
        with patch('chat_bot_template1.write_database', write_database):
                answer = corona_dynamics_write(self.update)
        self.assertNotEqual(answer, "")

    def test_equal_write(self):
        write_database = mock.MagicMock()
        self.corona.corona_dynamics()
        data = self.corona.now
        self.corona1.corona_dynamics()
        answer_2_0 = ''
        for elem in self.corona1.count[:5]:
            for key, value in self.corona1.now.items():
                for key1, value1 in data.items():
                    if key == key1 and value[4] == elem:
                        answer_2_0 += f'{str(value[0]).upper()}\n'
                        answer_2_0 += f'Confirmed: {value[1] - value1[1]} Deaths: {value[2] - value1[2]} Recovered: ' \
                            f'{value[3] - value1[3]} Active: {value[4] - value1[4]}\n'
        with patch('chat_bot_template1.write_database', write_database):
            answer = corona_dynamics_write(self.update)
        self.assertEqual(answer, answer_2_0)


class TestWriteCoronaRussia(unittest.TestCase):
    def setUp(self):
        self.update = mock.MagicMock()
        self.corona = WorkWithCoronaData([], count, [], [], {}, 1)
        self.corona1 = WorkWithCoronaData([], count, [], [], {}, 0)

    def test_ok_write(self):
        write_database = mock.MagicMock()
        with patch('chat_bot_template1.write_database', write_database):
                answer = corona_russia_write(self.update)
        self.assertNotEqual(answer, "")

    def test_equal_write(self):
        write_database = mock.MagicMock()
        self.corona.corona_russia()
        data = self.corona.now
        self.corona1.corona_russia()
        answer_2_0 = ''
        for key, value in self.corona1.now.items():
            for key1, value1 in data.items():
                answer_2_0 += f'{str(value[0]).upper()}\n'
                answer_2_0 += f'Confirmed: {value[1] - value1[1]} Deaths: {value[2] - value1[2]} Recovered: ' \
                    f'{value[3] - value1[3]} Active: {value[4] - value1[4]}\n'
        with patch('chat_bot_template1.write_database', write_database):
            answer = corona_russia_write(self.update)
        self.assertEqual(answer, answer_2_0)


if __name__ == '__main__':
    unittest.main()
