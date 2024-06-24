import json
import time

import allure
import pytest
import pytest_check as check
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from Common.find_element import find_element_wrap

driver = webdriver.Chrome()


class TestBossReport:

    def test_login_report(self):
        driver.get("https://boss-informal.rfsvr.net/auth/login")

        driver.delete_all_cookies()

        driver.refresh()

        with open('../TestData/login_cookies.json', 'r') as f:
            dict_cookies = json.load(f)

        for cookie in dict_cookies:
            driver.add_cookie(cookie)
            # print(cookie)

        driver.refresh()

        logo = find_element_wrap(driver, 'class name', 'logo-lg')

        check.is_true(logo)

    @pytest.mark.skip
    def test_request_cookie_login(self):
        url = 'https://boss-informal.rfsvr.net/'
        headers = {'Referer': 'https://boss-informal.rfsvr.net/auth/login'}

        cookies = {}
        with open('../TestData/login_cookies.json', 'r') as f:
            json_cookies = json.load(f)
        for cookie in json_cookies:
            cookies[cookie['name']] = cookie['value']

        print(cookies)

        response = requests.get(url, headers=headers, cookies=cookies)

        check.equal(response.status_code, 200)

    @allure.title('举报信息审核不通过')
    def test_report_boss(self):
        """driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list')
        # 创建一条举报数据
        url = 'https://rfs-fitness-informal.rfsvr.net/indoor/api/user/report'
        headers = {
            'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJkaXN0cmljdF9yZWxlYXNlIiwiaXNzIjoyMzg0OTIsInBsYXRmb3JtIjoyMiwibmJmIjoxNzE4Njc1NTQwLCJleHAiOjE3MTg3NjIwMDB9.Fl-1Q-TuzUsMydBe3NzZ8ATfNgjb_jeAenzM0SEOC3M',
            'UserId': '238492'
        }

        data = {"desc": "脚本测试", "source_id": 698, "reason_id": 3, "source_type": 1}

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            logger.info('添加举报数据成功')
        else:
            logger.info('添加举报数据失败')
        json_response = json.loads(response.text)
        report_id = json_response['data']['report_id']

        driver.get(f'https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id={report_id}')"""

        # 按id筛选举报列表页面
        driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=115')

        # 定位到table表格
        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')

        # 筛选后的举报列表，只有一条数据
        table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr')

        # 打开审核页面
        table.find_element(By.XPATH,
                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[11]/span/a').click()
        time.sleep(2)

        # 点击审核不通过
        table.find_element(By.XPATH,
                           '//*[@class="box-body no-padding"]/table/tbody/tr[1]/th/div/span/label[2]').click()

        # 点击确定按钮
        table.find_element(By.XPATH, '//*[@class="clearfix"]/div/a').click()

        time.sleep(0.5)

        # 处理alert弹窗
        alert = driver.switch_to.alert
        alert.accept()

        time.sleep(0.5)
        # 列表页的审核状态
        audit_status = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr/td[12]').text

        audit_1 = table.find_element(By.XPATH,
                                     '//*[@class="table table-hover grid-table"]/tbody/tr/td[14]').text
        # 列表页的审核方式
        audit_handle_method = table.find_element(By.XPATH,
                                                 '//*[@class="table table-hover grid-table"]/tbody/tr/td[15]').text
        audit_3 = table.find_element(By.XPATH,
                                     '//*[@class="table table-hover grid-table"]/tbody/tr/td[16]').text

        check.equal(audit_status, '审核未通过', '判断列表中的审核状态是否正确')
        check.equal(audit_1, '', '判断列表中的处理方式是否正确')
        check.equal(audit_handle_method, '', '判断列表中的处理方式是否正确')
        check.equal(audit_3, '', '判断列表中的处理方式是否正确')
