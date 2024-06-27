import json

from selenium import webdriver
from selenium.webdriver.common.by import By

from Common.find_element import find_element_wrap


def check_exist_punish(driver, data_key):
    driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/handle')
    tbody = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')
    target_tr = tbody.find_element(By.XPATH, f'//*[@data-key="{data_key}"]')

    data_key = (target_tr.get_attribute('data-key'))
    # 展开撤销
    target_tr.find_element(By.XPATH, f'//*[@data-key="{data_key}"]/td[12]/div/a').click()

    # 展开表单后，xpath路径中div元素的class属性发生变化
    # 点击撤销按钮
    target_tr.find_element(By.XPATH, f'//*[@data-key="{data_key}"]/td[12]/div/ul/li/a').click()


def login(driver):
    driver.get("https://boss-informal.rfsvr.net/auth/login")

    driver.delete_all_cookies()

    driver.refresh()
    with open('../TestData/login_cookies.json', 'r') as f:
        dict_cookies = json.load(f)

    for cookie in dict_cookies:
        driver.add_cookie(cookie)
        # print(cookie)

    driver.refresh()

    find_element_wrap(driver, 'class name', 'logo-lg')


if __name__ == '__main__':
    driver = webdriver.Chrome()
    login(driver)
    check_exist_punish(driver, 44)
