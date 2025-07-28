import os
import random
import time
from datetime import datetime

from faker import Faker
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, timeout=20)
fake = Faker()


def test_login():
    #To login to the application
    driver.get("https://thinking-tester-contact-list.herokuapp.com/")
    driver.find_element(By.ID, "email").send_keys("Supriyshetty02@yahoo.in");
    driver.find_element(By.ID, "password").send_keys("1234@Sup");
    driver.find_element(By.ID, "submit").click()
    capture_screenshot("test_login")
    assert "Contact List" in driver.title


def test_add_new_contact_to_the_list():
    wait.until(expected_conditions.presence_of_element_located((By.ID, "add-contact")))
    driver.find_element(By.ID, "add-contact").click()
    # Generate dynamic input
    first_name = fake.first_name()
    last_name = fake.last_name()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d")
    email = fake.email()
    phone = ''.join(random.choices('0123456789', k=10))
    street1 = fake.street_address()
    street2 = fake.secondary_address()
    city = fake.city()
    state = fake.state()
    postal_code = fake.postcode()
    country = fake.country()
    #Enterind the data in new contact creation page
    driver.find_element(By.ID, "firstName").send_keys(first_name)
    driver.find_element(By.ID, "lastName").send_keys(last_name)
    driver.find_element(By.ID, "birthdate").send_keys(birthdate)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "phone").send_keys(phone)
    driver.find_element(By.ID, "street1").send_keys(street1)
    driver.find_element(By.ID, "street2").send_keys(street2)
    driver.find_element(By.ID, "city").send_keys(city)
    driver.find_element(By.ID, "stateProvince").send_keys(state)
    driver.find_element(By.ID, "postalCode").send_keys(postal_code)
    driver.find_element(By.ID, "country").send_keys(country)
    capture_screenshot("test_add_new_contact_to_the_list")
    driver.find_element(By.ID, "submit").click()
    wait.until(expected_conditions.presence_of_element_located((By.ID, "add-contact")))


def test_edit_the_first_contact_list():
    # generating value for contry to update in edit contact list
    country = fake.country()

    # wait for contact list page
    wait.until(expected_conditions.presence_of_element_located((By.ID, "add-contact")))

    # fetch the current value of country in the first row
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='myTable']/tr[1]/td[8]")))
    country_value_before_updating = driver.find_element(By.XPATH, "//table[@id='myTable']/tr[1]/td[8]").text
    capture_screenshot("test_edit_the_first_contact_list")
    # edit the first row
    driver.find_element(By.XPATH, "//table[@id='myTable']/tr[1]").click()
    wait.until(expected_conditions.presence_of_element_located((By.ID, "edit-contact")))
    driver.find_element(By.ID, "edit-contact").click()
    time.sleep(1)

    # to clear the current country value
    driver.execute_script("document.getElementById('country').value = ''")
    time.sleep(1)
    # update the country field with new value
    driver.find_element(By.ID, "country").send_keys(country)
    driver.find_element(By.ID, "submit").click()
    # Return to contact list page
    wait.until(expected_conditions.presence_of_element_located((By.ID, "return")))
    driver.find_element(By.ID, "return").click()

    # verify country value is updated or not in contact list page
    wait.until(expected_conditions.presence_of_element_located((By.ID, "add-contact")))
    capture_screenshot("test_edit_the_first_contact_list")
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='myTable']/tr[1]/td[8]")))
    country_value_after_updating = driver.find_element(By.XPATH, "//table[@id='myTable']/tr[1]/td[8]").text
    assert country_value_before_updating != country_value_after_updating, "Country value did not update as expected"


def test_delete_the_first_contact_list():
    capture_screenshot("test_delete_the_first_contact_list")
    wait.until(expected_conditions.presence_of_element_located((By.ID, "add-contact")))
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='myTable']/tr")))
    no_of_rows_before_deleting = len(driver.find_elements(By.XPATH, "//table[@id='myTable']/tr"))
    driver.find_element(By.XPATH, "//table[@id='myTable']/tr[1]").click()
    wait.until(expected_conditions.presence_of_element_located((By.ID, "delete")))
    driver.find_element(By.ID, "delete").click()
    alert = driver.switch_to.alert
    alert.accept()
    wait.until(expected_conditions.presence_of_element_located((By.ID, "add-contact")))
    time.sleep(1)
    no_of_rows_after_deleting = len(driver.find_elements(By.XPATH, "//table[@id='myTable']/tr"))
    print(no_of_rows_after_deleting)
    capture_screenshot("test_delete_the_first_contact_list")
    assert no_of_rows_before_deleting == no_of_rows_after_deleting + 1, "Row was not deleted properly."


def test_logout():
    wait.until(expected_conditions.presence_of_element_located((By.ID, "add-contact")))
    capture_screenshot("test_logout")
    driver.find_element(By.ID, "logout").click()
    capture_screenshot("test_logout")
    driver.quit()


def capture_screenshot(test_name):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join("reports", "screenshots")
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{test_name}_{timestamp}.png"
    full_path = os.path.join(folder_path, filename)
    driver.save_screenshot(full_path)

