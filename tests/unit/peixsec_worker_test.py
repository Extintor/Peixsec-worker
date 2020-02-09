import unittest
from unittest import mock
import os

from peixsec_worker import peixsec_worker


class PeixSecTests(unittest.TestCase):

    def setUp(self) -> None:
        self.process_mock = mock.MagicMock()

    @mock.patch('subprocess.Popen')
    @mock.patch('peixsec_worker.peixsec_worker.MongoClient')
    @mock.patch('pika.BlockingConnection')
    @mock.patch('pika.ConnectionParameters')
    def test_process_channel_db_single_call(self, conn_params_mock, block_conn_mock, mongoclient_mock, popen_mock):
        peixsec_worker.main()
        block_conn_mock.return_value.channel.called_once()
        mongoclient_mock.assert_called_once()
        popen_mock.assert_called_once_with('stockfish', universal_newlines=True, stdin=-1, stdout=-1, bufsize=1)

    def test_get_db_credentials(self):
        os.environ['DB_USER'] = 'test_user'
        os.environ['DB_PASSWORD'] = 'test_password'
        user, password = peixsec_worker._get_db_credentials()
        self.assertEqual(user, 'test_user')
        self.assertEqual(password, 'test_password')

    def test_write_stdin(self):
        peixsec_worker._write_stdin(self.process_mock, 'test_command')
        self.process_mock.stdin.write.called_with('test_command')
        self.process_mock.stdin.flush.called_once()

    def test_get_best_move(self):
        self.process_mock.stdout = ['bestmove test']
        move = peixsec_worker._get_best_move(self.process_mock)
        self.assertEqual(move, 'test')

    def test_process_position(self):
        collection_mock = mock.MagicMock()
        peixsec_worker.process_position('test_str', self.process_mock, collection_mock)
        collection_mock.insert_one.called_once()
