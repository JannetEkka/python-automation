from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from base.base_driver import BaseDriver
from pages.search_flights_results_page import SearchFlightsResult
from utilities.utils import Utils
from selenium.webdriver.common.action_chains import ActionChains

class LaunchPage(BaseDriver):

    log = Utils.customLogger()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    #locators
    DEPART_FROM_FIELD = 'BE_flight_origin_city'
    GOING_TO_FIELD = "BE_flight_arrival_city"
    SEARCH_RESULTS = "//div[@class='viewport']//div[1]/li"
    DEPART_DATE = "//input[@id='BE_flight_origin_date']"
    ALL_DEPART_DATES = '//div[@class="day-container"]//td[@class!="inActiveTD"]'
    SEARCH_FLIGHTS_BTN = "//input[@value='Search Flights']"
    
    #externalize locator
    def getDepartFromField(self):
        return self.wait_until_element_is_clickable(By.ID,self.DEPART_FROM_FIELD)
    
    def getGoingToField(self):
        return self.wait_until_element_is_clickable(By.ID,self.GOING_TO_FIELD)
    
    def getSearchBtn(self):
        return self.driver.find_element(By.XPATH,self.SEARCH_FLIGHTS_BTN)

    def getSearchResults(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.SEARCH_RESULTS)
    
    def getDepartDateField(self):
        return self.wait_until_element_is_clickable(By.XPATH,self.DEPART_DATE)
    
    def getAllDates(self):
        return self.wait_until_element_is_clickable(By.XPATH,self.ALL_DEPART_DATES)
    
    #actions on locator
    def enterDepartFromField(self, departlocation):
        self.getDepartFromField().click()
        self.log.info('Clicked on Departure From Location')
        time.sleep(2)
        self.getDepartFromField().send_keys(departlocation)
        self.log.info('Entered Location')
        time.sleep(2)
        self.getDepartFromField().send_keys(Keys.ENTER) 
        self.log.info('Searched for Location')  
    
    def enterGoingToField(self,goingtolocation):
        self.getGoingToField().click()
        self.log.info('Clicked on Going To Location')
        time.sleep(2)
        self.getGoingToField().send_keys(goingtolocation)
        self.log.info('Searched for Location')
        time.sleep(3)

        search_results = self.getSearchResults()
        for results in search_results:
            if goingtolocation in results.text:
                results.click()
                self.log.info('Clicked on Going To Location')
                break

    def selectDepartureDate(self,departure_date):
        self.getDepartDateField().click()
        self.log.info('Departure Date field is clicked. Calendar pop-up opened.')
        all_dates=self.getAllDates().find_elements(By.XPATH,self.ALL_DEPART_DATES)
        self.log.info('All dates are found and present')
        for date in all_dates:
            if date.get_attribute('data-date')==departure_date:
                date.click()
                self.log.info('date selected is clicked')
                break

        # time.sleep(2)
        # date_field = self.getDepartDateField()
        # date_field.click()
        # self.log.info('Departure Date field is clicked')

        # self.page_scroll()

        # departure_dates = self.getAllDates()
        # self.log.info('All dates are present')
        # departure_dates_list = [date.get_attribute('data-date') for date in departure_dates if date.get_attribute('data-date')]
        # self.log.info('Got all departure dates in our list and they dont have null values')

        # for date_element, date in zip(departure_dates, departure_dates_list):
        #     # self.log.debug('print departure date',departure_date,date,type(departure_date))
        #     if date == departure_date:
        #         # self.log.info('print departure date',departure_date)
        #         # self.wait_until_element_is_clickable(date_element)
        #         # actions = ActionChains(self.driver)
        #         # actions.move_to_element(date_element).perform()
        #         # self.log.info('Scrolled to the dep date within the calendar popup')
        #         # self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight));")
        #         self.driver.execute_script("arguments[0].scrollIntoView().click();", date)
        #         self.log.info('date requested is found and clicked')
        #         break

    def searchFlights(self,departlocation,goingtolocation,departure_date):
        self.enterDepartFromField(departlocation)
        time.sleep(2)
        self.enterGoingToField(goingtolocation)
        time.sleep(2)
        self.selectDepartureDate(departure_date)
        time.sleep(2)
        self.clicksearch()
        search_flight_res = SearchFlightsResult(self.driver)
        return search_flight_res   
    
    def clicksearch(self):
        self.getSearchBtn().click()
        self.log.info('clicked search flights button')
        time.sleep(5)

