import pytest
import unittest
from pages.login_page import LoginPage
from pages.dashboard import Dashboard
import base.custom_logger as cl
import logging


class NewTest1(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, setUp):
        self.lp = LoginPage(self.driver)
        self.dashboard = Dashboard(self.driver)
        self.log = cl.customLogger(logging.DEBUG)

    def test_1(self):
        self.log.info("STARTING TEST_1")
        assert self.lp.login("Noam1","Noam123") != False, "failed to login"
        assert self.dashboard.verifyDashboardPageDisplay()!= False
        assert self.dashboard.selectRange("Last 3 Days") != False, "failed to select date range"
        assert self.dashboard.verifyRangeSelcted("3") != False, "failed tp verify select range "



    def test_2(self):
        self.log.info("STARTING TEST_2")
        assert self.dashboard.comperTotalSpend("QA Client", "Offers")!=False, "failed, total spend isn't equal"
        print()