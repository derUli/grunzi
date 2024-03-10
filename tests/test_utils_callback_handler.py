import unittest

from utils.callbackhandler import CallbackHandler


class CallbackHandlerTest(unittest.TestCase):

    def test_constructor(self):
        callback_handler = CallbackHandler(on_complete=self.on_complete)
        self.assertEqual('on_complete called', callback_handler.on_complete())

    def on_complete(self):
        return 'on_complete called'
