import time
import softest
import pytest
from pages.yatra_launch_page import LaunchPage
from utilities.utils import Utils
from utilities.utils import Utils
import logging
from ddt import ddt, file_data,data,unpack

@pytest.mark.usefixtures("setup")
@ddt
class TestYatraDemo(softest.TestCase):
    log = Utils.customLogger()
    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = LaunchPage(self.driver)
        self.ut = Utils()
    
    # @file_data("../testdata/testdata.json")
    @data(*Utils.read_data_from_excel("D:\\Projects\\Automation\\python-automation\\Yatra\\testdata\\tdataexcel.xlsx","Sheet1"))
    @unpack
    def test_searchflights_1stop(self,goingFrom,goingTo,depDate,stops):
        search_flight_res = self.lp.searchFlights(goingFrom,goingTo,depDate)
        self.lp.page_scroll()
        search_flight_res.filter_flights_by_stop(stops)
        allstops1 = search_flight_res.get_search_results_from_filters()
        self.log.info(len(allstops1))
        self.ut.assertListItemText(allstops1,stops)
        time.sleep(3)



