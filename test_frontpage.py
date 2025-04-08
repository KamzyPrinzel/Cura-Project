import time
from datetime import datetime, timedelta
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://katalon-demo-cura.herokuapp.com/"
username = "John Doe"
password = "ThisIsNotAPassword"

@pytest.fixture
def test_browser():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()

@allure.feature("Frontpage")
@pytest.mark.usefixtures("test_browser")
def test_url(test_browser):
    with allure.step("Open main page"):
        test_browser.get(url)
        assert test_browser.title == "CURA Healthcare Service"

    allure.attach(test_browser.get_screenshot_as_png(),
                  name="Main page",
                  attachment_type=allure.attachment_type.PNG)

    with allure.step("log in"):
        test_browser.find_element(By.XPATH, value="//i[@class='fa fa-bars']").click()
        time.sleep(1)

        test_browser.find_element(By.LINK_TEXT, value="Login").click()
        time.sleep(1)

        allure.attach(test_browser.get_screenshot_as_png(),
                      name="Login page",
                      attachment_type=allure.attachment_type.PNG)

        test_browser.find_element(By.XPATH, value="//input[@id='txt-username']").send_keys(username)
        time.sleep(1)
        test_browser.find_element(By.XPATH, value="//input[@id='txt-password']").send_keys(password)
        time.sleep(1)
        test_browser.find_element(By.ID, value='btn-login').click()
        time.sleep(1)
        assert test_browser.current_url == "https://katalon-demo-cura.herokuapp.com/#appointment"

        allure.attach(test_browser.get_screenshot_as_png(),
                      name="Dashboard page",
                      attachment_type=allure.attachment_type.PNG)


    with allure.step("Handle the dropdown"):
        dropdown_element = test_browser.find_element(By.ID, value="combo_facility")
        select = Select(dropdown_element)
        select.select_by_visible_text("Hongkong CURA Healthcare Center")
        time.sleep(1)

    with allure.step("Handling the checkbox"):
        checkbox_element = test_browser.find_element(By.XPATH, value="//input[@id='chk_hospotal_readmission']")
        checkbox_element.click()

    with allure.step("Handling the radio button"):
        radio_button_element = test_browser.find_element(By.XPATH, value="//input[@id='radio_program_medicaid']")
        radio_button_element.click()

    with allure.step("Handling the date picker"):
        test_browser.find_element(By.XPATH, value="//input[@id='txt_visit_date']")

        test_browser.find_element(By.CSS_SELECTOR, value= ".glyphicon.glyphicon-calendar").click()
        time.sleep(1)

        current_date = datetime.now()
        next_date = current_date + timedelta(days=1)
        formatted_date = next_date.strftime("%d/%m/%Y")
        test_browser.find_element(By.CSS_SELECTOR, value="#txt_visit_date").send_keys(formatted_date)
        time.sleep(1)

    with allure.step("Handling the Comment box"):
        text_editor = test_browser.find_element(By.TAG_NAME, value="textarea")
        text_editor.clear()
        text_editor.send_keys("I want to book an appointment for tomorrow")
        time.sleep(3)

    with allure.step("Click on the submit button"):
        test_browser.find_element(By.ID, value="btn-book-appointment").click()
        time.sleep(2)

        element = WebDriverWait(test_browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-default']"))
        )
        test_browser.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(test_browser, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//a[@class='btn btn-default']")
        )).click()
        time.sleep(2)
