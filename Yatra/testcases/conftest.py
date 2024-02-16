import os
import time
import pytest_html
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
driver = None

@pytest.fixture(autouse=True)
def setup(request,browser):
    global driver
    if browser == 'chrome':
        print('Launching Chrome')
        driver = webdriver.Chrome()
    elif browser == 'ff':
        print('Launching Firefox')
        driver = webdriver.Firefox()
    elif browser == 'edge':
        print('Launching Edge')
        driver = webdriver.Edge()
    request.cls.driver = driver
    driver.get("https://www.yatra.com/")
    driver.maximize_window()
    
    yield
    driver.close()

def pytest_addoption(parser):
    parser.addoption("--browser")

@pytest.fixture(scope="class",autouse=True)
def browser(request):
    return request.config.getoption("--browser")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        # always add url to report
        extras.append(pytest_html.extras.url("http://www.Yatra.com/"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = str(int(round(time.time() * 1000))) + ".png"
            # file_name = report.nodeid.replace("::", "_") + ".png"
            destinationFile = os.path.join(report_directory, file_name)
            driver.save_screenshot(destinationFile)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:300px;height=200px" ' \
                       'onclick="window.open(this.src)" align="right"/></div>'%file_name
            extras.append(pytest_html.extras.html(html))
        report.extras = extras

def pytest_html_report_title(report):
    report.title = "Yatra Automation Report"