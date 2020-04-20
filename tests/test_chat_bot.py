# -*- coding: utf-8 -*-
from io import StringIO
import unittest
from unittest import mock
from unittest.mock import patch

from chat_bot_template1 import array, write_history,facts,corona,corona_dynamics,corona_russia,analise

@analise
def simple_action(update):
    return None

new_array= []
new_array1= []
class TestsLogs(unittest.TestCase):
    def setUp(self):
        self.update = mock.MagicMock()

    def tearDown(self):
        global array
        array = []

    def test_log_action(self):
        self.update.message.text = "hi"
        self.update.effective_user.first_name = "Miki"
        simple_action(self.update)
        self.assertEqual(array[-1], [{'user': 'Miki', 'function': 'simple_action', 'message': 'hi'}])

    def test_no_message(self):
        self.update = mock.MagicMock(spec=['effective_user'])
        simple_action(self.update)
        self.assertEqual(array, [])

    def test_no_user(self):
        self.update = mock.MagicMock(spec=['message'])
        simple_action(self.update)
        self.assertEqual(array, [])

    def test_none_update(self):
        self.update=None
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
            reply_text=write_history(self.update,[])
        self.assertEqual(reply_text, [])

    @patch('chat_bot_template1.array', new_array1)
    def test_history(self):
        new_array1.append({'user': '1',
               'function': 'func1',
               'message': 'hello',
               })
        mock_open_handler = mock.mock_open()
        with patch('chat_bot_template1.open', mock_open_handler):
            reply_text=write_history(self.update,new_array1)

        self.assertEqual(reply_text, ['Action 1:','user : 1','function : func1', 'message : hello'])

    @patch('chat_bot_template1.array', new_array)
    def test_history_no_user(self):
        self.update.effective_user.first_name = None
        mock_open_handler = mock.mock_open()
        with patch('chat_bot_template1.open', mock_open_handler):
            reply_text = write_history(self.update,new_array)
        self.assertEqual(reply_text, [])


if __name__ == '__main__':
    unittest.main()
