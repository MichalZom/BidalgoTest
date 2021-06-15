from selenium.webdriver.common.by import By
import base.custom_logger as cl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver


    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator + " locatorType: " + locatorType)
            return False
        return element

    # Either provide element or a combination of locator and locatorType
    def elementClick(self, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator +
                          " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator +" locatorType: " + locatorType)
            return False

    # Either provide element or a combination of locator and locatorType
    def sendKeys(self, data, locator="", locatorType="id", element=None):
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            return False


    def waitForElement(self, locator, locatorType="id", timeout=10):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((byType, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            return False
        return element


    def getElementAttribute(self, element, attributeName):
        try:
            attributeValue = element.get_attribute(attributeName)
        except:
            self.log.info("Cannot find element attribute: " + attributeName)
            return False
        return  attributeValue

    def getElementList(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elementList = self.driver.find_elements(byType, locator)
            self.log.info("Element list found with locator: " + locator +" and  locatorType: " + locatorType)
        except:
            self.log.info("Element list not found with locator: " + locator + " and  locatorType: " + locatorType)
            return False
        return elementList