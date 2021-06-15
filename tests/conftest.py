import pytest
from base.webdriverfactory import WebDriverFactory


@pytest.fixture(scope="class")
def setUp(request,browser):
    print("Running setUp")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()
    if request.cls is not None:
        request.cls.driver = driver

    yield
    driver.quit()
    print("Running tearDown")


def pytest_addoption(parser):
    parser.addoption("--browser")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")
