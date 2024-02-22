import logging
import time
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils

class SearchFlightsResult(BaseDriver):

    log = Utils.customLogger(loglevel=logging.WARNING)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        # self.wait = wait
    #locators
    FILTER_BY_1_STOP_ICON = "//p[@class='font-lightgrey bold'][normalize-space()='1']"
    FILTER_BY_2_STOP_ICON = "//p[@class='font-lightgrey bold'][normalize-space()='2']"
    FILTER_BY_0_STOP_ICON = "//p[@class='font-lightgrey bold'][normalize-space()='0']"
    FILTER_BY_STOP_OPTION = '//span[contains(text(),"1 Stop") or contains(text(),"2 Stop(s)") or contains(text(),"Non Stop")]'

    def getFilterBy1(self):
        return self.driver.find_element(By.XPATH,self.FILTER_BY_1_STOP_ICON)
    
    def getFilterBy2(self):
        return self.driver.find_element(By.XPATH,self.FILTER_BY_2_STOP_ICON)

    def getFilterBy0(self):
        return self.driver.find_element(By.XPATH,self.FILTER_BY_0_STOP_ICON)

    def filter_flights_by_stop(self,by_stop):
        if by_stop == "1 Stop":
            self.getFilterBy1().click()
            self.log.info('Selected Flights with 1 Stop')
            time.sleep(3)
        elif by_stop == "2 Stop(s)":
            self.getFilterBy2().click()
            self.log.info('Selected Flights with 2 Stops')
            time.sleep(3)
        elif by_stop == "Non Stop":
            self.getFilterBy0().click()
            self.log.info('Selected Flights with Non Stop')
            time.sleep(3)
        else:
            self.log.warning('Please provide valid filter option')

    def get_search_results_from_filters(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.FILTER_BY_STOP_OPTION)

    