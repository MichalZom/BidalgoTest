from base.selenium_driver import SeleniumDriver
import base.custom_logger as cl
import logging


class LoginPage(SeleniumDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _wellcome_message = "signInHeader"
    _user_name_field = "user_name"
    _password_field = "user_pass"
    _continue_button = "button[type=submit]"

    log = cl.customLogger(logging.DEBUG)


    def enterEmail(self, user):
        self.log.info("enter 'user name'")
        if self.sendKeys(user, self._user_name_field) == False:
            self.log.info("can't insert user name")
            return False

    def enterPassword(self, password):
        self.log.info("enter 'Password'")
        if self.sendKeys(password, self._password_field) == False:
            self.log.info("can't insert password")
            return False

    def clickContinueButton(self):
        self.log.info("enter 'clickLoginButton'")
        if self.elementClick(self._continue_button, locatorType="css") == False:
            self.log.info("can't click on continue button")
            return False

    def login(self, user, password):
        self.log.info("enter 'login' function")
        assert self.waitForElement(self._wellcome_message) != False, "login page isn't display"
        assert self.enterEmail(user) != False, "failed to insert user name"
        assert self.enterPassword(password) != False, "failed to insert password"
        assert self.clickContinueButton() != False, "failed to click on continue button"

