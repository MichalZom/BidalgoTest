from base.selenium_driver import SeleniumDriver
import base.custom_logger as cl
import logging
import time

class Dashboard(SeleniumDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _dashboard_body = "div.panel-body"
    _date_picker_button = "//button[contains(@class, 'date-picker-btn')]"
    _picker_range_button = "div.range-button"
    _select_range = "//div[@data-range-key='{}']"
    _apply_button = "button.applyBtn.btn"
    _app_name = "//a[@title='{}']"
    _applications_table = "div.ag-center-cols-container"
    _app_row = "//div[@row-id='{}']"
    _total_spend_app_tab = "//span[@aria-colindex='3']"
    _tab_name_active = "//li[@class='active']"
    _offers_tab_bottom_container = "div.ag-floating-bottom-container"
    _total_spend_offers_tab = "div[aria-colindex='5'][role='gridcell']"


    log = cl.customLogger(logging.DEBUG)


    def verifyDashboardPageDisplay(self):
        self.log.info("enter 'verifyDashboardPageDisplay'")
        if self.waitForElement(self._dashboard_body, locatorType="css", timeout=40) == False:
            self.log.info("dashboard page isn't display")
            return False

    def openDatePicker(self):
        if self.elementClick(self._date_picker_button, locatorType="xpath") == False:
            self.log.info("can't open date picker")
            return False

    def openPickerRange(self):
        if self.elementClick(self._picker_range_button, locatorType="css") == False:
            self.log.info("can't open date picker range button")
            return False

    def selectDateRange(self, range):
        tmpxpath = self._select_range.format(range)
        if self.elementClick(tmpxpath, locatorType="xpath") == False:
            self.log.info("can't choose range '" + range + "'")
            return False

    # in the function i'm only verifying the scenario that i tested but in real the function need to be divided to
    # cases according the options
    def verifyRangeSelcted(self, range):
        datePicker = self.getElement(self._date_picker_button, locatorType="xpath").text
        if range not in datePicker:
            self.log.info("selected range isn't correct")
            return False
        time.sleep(2)


    def selectRange(self, range):
        assert self.openDatePicker() != False
        assert self.openPickerRange() != False
        assert self.selectDateRange(range) != False
        assert self.elementClick(self._apply_button, locatorType="css") != False, "cant click on apply button"


    def getTotalMediaSpendOnApp(self, appName):
#        breakpoint()
        rowNumber = self.findAppRowNumberInAppsTab(appName)
        assert rowNumber != False , "can't find row number for app: " + appName
        totalSpend = self.totalSpendByRowInAppsTab(rowNumber)
        assert totalSpend != None, "can't find total spend for app: " + appName
        return totalSpend


    def findAppRowNumberInAppsTab(self, appName):
        tmpXpath = self._app_name.format(appName)
        appEl = self.getElement(tmpXpath, locatorType="xpath")
        if appEl == False:
            self.log.info("can't find app '" + appName + "' element")
            return False
        try:
            appPerent = appEl.find_element_by_xpath("../../../../..")
        except:
            self.log.info("can't find app '" + appName + "' parent element")
            return False

        rowNumber = self.getElementAttribute(appPerent, "row-id")
        if rowNumber == None:
            self.log.info("can't find app '" + appName + "' row number")
            return False

        return rowNumber


    def totalSpendByRowInAppsTab(self, rowNumber):
        tableEl = self.getElement(self._applications_table, locatorType="css")
        if tableEl == False:
            self.log.info("can't find application table element")
            return False

        tablelist = tableEl.find_elements_by_xpath(self._total_spend_app_tab)
        if tablelist == False:
            self.log.info("can't find table total spend elements")
            return False

        for item in tablelist:
            try:
                tmpParent = item.find_element_by_xpath("../../..")
            except:
                self.log.info("can't find element parent")
                return False
            number = self.getElementAttribute(tmpParent,"row-id")
            if rowNumber == number:
                return item.text

        self.log.info("did not found total spend match to row: " + rowNumber)
        return False


    def clickOnAppName(self, appName):
        tmpXpath = self._app_name.format(appName)
        if self.elementClick(tmpXpath, locatorType="xpath") == False:
            self.log.info("can't click on application name")
            return False
        time.sleep(2)

    def verifyTabDisplay(self, tabName):
        tabEl = self.getElement(self._tab_name_active, locatorType="xpath")
        if tabEl == False:
            self.log.info("can't find tab active element")
            return False

        if tabEl.text != tabName:
            self.log.info("tab '" + tabName + "' isn't display")
            return False


    def findTotalInOffresTab(self):
        time.sleep(1)
        containerEl = self.getElement(self._offers_tab_bottom_container, locatorType="css")
        if containerEl == False:
            self.log.info("can't find container element")
            return False
        time.sleep(2)

        try:
            total = (containerEl.find_element_by_css_selector(self._total_spend_offers_tab)).text
        except:
            self.log.info("can't find total spend element")
            return False
        return total

    def comperTotalSpend(self, appName, tabName):
        appTabSpend = self.getTotalMediaSpendOnApp(appName)
        if appTabSpend == False:
            self.log.info("failed to get total media  in app tab")
            return False

        if self.clickOnAppName(appName) == False:
            self.log.info("failed to click on app '" + appName + "'")
            return False

        if self.verifyTabDisplay(tabName) == False:
            self.log.info("failed verify offers tab display")
            return False

        offersTabSpend = self.findTotalInOffresTab()
        if offersTabSpend == False:
            self.log.info("failed to get total media spend in offers tab")
            return False

        assert appTabSpend == offersTabSpend, "total spend isn't equal between app tab and offers tab"