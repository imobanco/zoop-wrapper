import unittest

from ZoopAPIWrapper.zoop import Zoop
from ZoopAPIWrapper.constants import ZOOP_KEY, MARKETPLACE_ID, MAIN_SELLER


class TestZoop(unittest.TestCase):

    def setUp(self):
        self.zoop = Zoop(MARKETPLACE_ID, ZOOP_KEY)

    def tearDown(self):
        del self.zoop

    def test_search_seller_by_id(self):
        response_as_dict = self.zoop.search_seller_by_id(MAIN_SELLER)
        print(response_as_dict)

    # def test_get_bank_account(self):
    #     response_as_dict = self.zoop.get_bank_account(MAIN_SELLER)
    #     print(response_as_dict)
    #
    # def test_list_transactions(self):
    #     response_as_dict = self.zoop.list_transactions(MAIN_SELLER)
    #     print(response_as_dict)


if __name__ == '__main__':
    unittest.main()
