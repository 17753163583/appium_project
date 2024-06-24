from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def find_element_wrap(driver, find_type, find_key):
    try:
        element = WebDriverWait(driver, 10, 0.25).until(ec.visibility_of_element_located((find_type, find_key)))
        return element
    except Exception as e:
        raise e
