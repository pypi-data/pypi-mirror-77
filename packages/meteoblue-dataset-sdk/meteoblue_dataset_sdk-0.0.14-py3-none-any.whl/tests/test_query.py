import unittest
from meteoblue_dataset_sdk import Client


class Test_TestQuery(unittest.TestCase):
    def test_1(self):
        c = Client("awdawd")
        print(c)
