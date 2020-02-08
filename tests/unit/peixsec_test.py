import unittest
from unittest import mock

from peixsec import peixsec


class PeixSecTests(unittest.TestCase):

    def setUp(self) -> None:
        self.connection_params_mock = mock.patch('pika.ConnectionParameters').start()
        self.connection_mock = mock.patch('pika.BlockingConnection').start()
        self.channel = self.connection_mock.return_value.channel

    def test_channel_single_call(self):
        peixsec.main()
        self.channel.assert_called_once()

    def test_stop_when_keyboard_interrupt(self):
        self.channel.return_value.start_consuming.side_effect = KeyboardInterrupt
        peixsec.main()
        self.channel.return_value.stop_consuming.assert_called()
