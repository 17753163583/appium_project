import json
import time

from selenium import webdriver

driver = webdriver.Chrome()


def login_cookies():
    driver.get("https://boss-informal.rfsvr.net/auth/login")

    time.sleep(15)

    dict_cookies = driver.get_cookies()
    json_cookies = json.dumps(dict_cookies)
    # print(json_cookies)
    with open('../TestData/login_cookies.json', 'w') as f:
        f.write(json_cookies)

    driver.delete_all_cookies()

    driver.refresh()

    with open('../TestData/login_cookies.json', 'r') as f:
        dict_cookies = json.load(f)

    for cookie in dict_cookies:
        driver.add_cookie(cookie)
        # print(cookie)

    driver.maximize_window()

    driver.refresh()
    time.sleep(5)


if __name__ == '__main__':
    login_cookies()
