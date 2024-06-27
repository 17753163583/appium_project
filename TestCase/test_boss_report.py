import json
import time

import allure
import pytest
import pytest_check as check
import requests
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from Common.check_exist_punish import check_exist_punish
from Common.find_element import find_element_wrap
from Common.logger import log_decorator

driver = webdriver.Chrome()


class TestBossReport:
    @allure.title("BOSS登录")
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
    @allure.title("请求使用cookie登录boss")
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

    @log_decorator
    @allure.title('举报信息审核不通过')
    @pytest.mark.skip
    def test_report_boss(self, add_report_requests):

        driver.get(f'https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id={add_report_requests}')

        """ # 按id筛选举报列表页面
        driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=115')"""

        # 定位到table表格
        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')

        # 筛选后的举报列表，只有一条数据
        table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr')

        # 打开审核页面
        table.find_element(By.XPATH,
                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[11]/span/a').click()

        # 点击审核不通过
        table.find_element(By.XPATH,
                           '//*[@class="box-body no-padding"]/table/tbody/tr[1]/th/div/span/label[2]').click()

        # 点击确定按钮
        table.find_element(By.XPATH, '//*[@class="clearfix"]/div/a').click()

        # alert弹窗有延迟
        time.sleep(1)

        # 处理alert弹窗
        alert = driver.switch_to.alert
        alert.accept()

        driver.refresh()

        # 刷新之后，父节点定位失效，重新定位
        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')
        # 列表页的审核状态
        audit_status = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr/td[12]').text

        violations_reason = table.find_element(By.XPATH,
                                               '//*[@class="table table-hover grid-table"]/tbody/tr/td[14]').text
        # 列表页的审核方式
        audit_handle_method = table.find_element(By.XPATH,
                                                 '//*[@class="table table-hover grid-table"]/tbody/tr/td[15]').text
        audit_message = table.find_element(By.XPATH,
                                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[16]').text

        check.equal(audit_status, '审核未通过', '判断列表中的审核状态是否正确')
        logger.info(f'审核状态：{audit_status}')

        check.equal(violations_reason, '', '判断列表中的违规原因是否正确')
        logger.info(f'违规原因：{violations_reason}')

        check.equal(audit_handle_method, '', '判断列表中的处理方式是否正确')
        logger.info(f'处理方式{audit_handle_method}')

        check.equal(audit_message, '', '判断列表中的备注是否正确')
        logger.info(f'备注{audit_message}')

    @log_decorator
    @pytest.mark.skip
    @allure.title('举报信息审核通过_通知警告')
    def test_boss_report_pass_notice(self, add_report_requests):
        # 按id筛选举报列表页面
        driver.get(f'https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id={add_report_requests}')

        """ 
        driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=115')"""

        # 定位到table表格
        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')

        # 筛选后的举报列表，只有一条数据
        tr = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr')

        data_key = tr.get_attribute('data-key')

        # 打开审核页面
        table.find_element(By.XPATH,
                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[11]/span/a').click()
        time.sleep(2)

        # 点击审核通过
        table.find_element(By.XPATH,
                           '//*[@class="box-body no-padding"]/table/tbody/tr[1]/th/div/span/label[1]').click()

        # 定位到处理方式下拉框
        select = table.find_element(By.XPATH,
                                    '//*[@class="box-body no-padding"]/table/tbody/tr[3]/th/div/span[1]/select')
        # 选择通知警告
        Select(select).select_by_value('is_notice_warning')

        time.sleep(2)
        # 点击确定按钮
        table.find_element(By.XPATH, '//*[@class="clearfix"]/div/a').click()

        # alert弹窗有延迟
        time.sleep(1)

        # 处理alert弹窗
        alert = driver.switch_to.alert
        alert.accept()

        driver.refresh()

        # 刷新之后，父节点定位失效，重新定位
        # 不刷新无法更新审核状态（开发实现如此）

        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')
        # 列表页的审核状态
        audit_status = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr/td[12]').text

        violations_reason = table.find_element(By.XPATH,
                                               '//*[@class="table table-hover grid-table"]/tbody/tr/td[14]').text
        # 列表页的审核方式
        audit_handle_method = table.find_element(By.XPATH,
                                                 '//*[@class="table table-hover grid-table"]/tbody/tr/td[15]').text
        audit_message = table.find_element(By.XPATH,
                                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[16]').text

        check.equal(audit_status, '审核通过', '判断列表中的审核状态是否正确')
        logger.info(f'审核状态：{audit_status}')

        check.equal(violations_reason, '暴力恐怖', '判断列表中的违规原因是否正确')
        logger.info(f'违规原因：{violations_reason}')

        check.equal(audit_handle_method, '通知警告', '判断列表中的处理方式是否正确')
        logger.info(f'处理方式{audit_handle_method}')

        check.equal(audit_message, '', '判断列表中的备注是否正确')
        logger.info(f'备注{audit_message}')

    @log_decorator
    @pytest.mark.skip
    @allure.title('举报信息审核通过_通知警告')
    def test_boss_report_pass_notice(self, add_report_requests):
        # 按id筛选举报列表页面
        driver.get(f'https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id={add_report_requests}')

        """ 
        driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=115')"""

        # 定位到table表格
        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')

        # 筛选后的举报列表，只有一条数据
        table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr')

        # 打开审核页面
        table.find_element(By.XPATH,
                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[11]/span/a').click()
        time.sleep(2)

        # 点击审核通过
        table.find_element(By.XPATH,
                           '//*[@class="box-body no-padding"]/table/tbody/tr[1]/th/div/span/label[1]').click()

        # 定位到处理方式下拉框
        select = table.find_element(By.XPATH,
                                    '//*[@class="box-body no-padding"]/table/tbody/tr[3]/th/div/span[1]/select')
        # 选择通知警告
        Select(select).select_by_value('is_notice_warning')

        # 点击确定按钮
        table.find_element(By.XPATH, '//*[@class="clearfix"]/div/a').click()

        # alert弹窗有延迟
        time.sleep(1)

        # 处理alert弹窗
        alert = driver.switch_to.alert
        alert.accept()

        driver.refresh()

        # 刷新之后，父节点定位失效，重新定位
        # 不刷新无法更新审核状态（开发实现如此）

        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')
        # 列表页的审核状态
        audit_status = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr/td[12]').text

        violations_reason = table.find_element(By.XPATH,
                                               '//*[@class="table table-hover grid-table"]/tbody/tr/td[14]').text
        # 列表页的审核方式
        audit_handle_method = table.find_element(By.XPATH,
                                                 '//*[@class="table table-hover grid-table"]/tbody/tr/td[15]').text
        audit_message = table.find_element(By.XPATH,
                                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[16]').text

        check.equal(audit_status, '审核通过', '判断列表中的审核状态是否正确')
        logger.info(f'审核状态：{audit_status}')

        check.equal(violations_reason, '暴力恐怖', '判断列表中的违规原因是否正确')
        logger.info(f'违规原因：{violations_reason}')

        check.equal(audit_handle_method, '通知警告', '判断列表中的处理方式是否正确')
        logger.info(f'处理方式{audit_handle_method}')

        check.equal(audit_message, '', '判断列表中的备注是否正确')
        logger.info(f'备注{audit_message}')

    # 第二次调用时，记得撤销处罚
    @log_decorator
    @allure.title('举报信息审核通过_禁言1小时')
    @pytest.mark.skip
    def test_boss_report_pass_silence_hours(self, add_report_requests):
        # 按id筛选举报列表页面
        driver.get(f'https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id={add_report_requests}')

        """ 
        driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=115')"""

        # 定位到table表格
        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')

        # 筛选后的举报列表，只有一条数据
        tr = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr')

        data_key = tr.get_attribute('data-key')

        # 打开审核页面
        table.find_element(By.XPATH,
                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[11]/span/a').click()
        time.sleep(1)

        # 点击审核通过
        table.find_element(By.XPATH,
                           '//*[@class="box-body no-padding"]/table/tbody/tr[1]/th/div/span/label[1]').click()

        # 定位到处理方式下拉框
        select = table.find_element(By.XPATH,
                                    '//*[@class="box-body no-padding"]/table/tbody/tr[3]/th/div/span[1]/select')
        # 选择禁言
        Select(select).select_by_value('is_forbid_speak')

        # 禁言1小时
        input_box = table.find_element(By.XPATH,
                                       '//*[@class="box-body no-padding"]/table/tbody/tr[3]/th/div/span[2]/span[1]/input')
        # 全选删除后，输入1
        input_box.send_keys(Keys.CONTROL + 'a')
        input_box.send_keys(Keys.BACKSPACE)
        input_box.send_keys(1)

        # 点击确定按钮
        table.find_element(By.XPATH, '//*[@class="clearfix"]/div/a').click()

        # alert弹窗有延迟
        time.sleep(1)

        # 处理alert弹窗
        alert = driver.switch_to.alert
        alert.accept()

        driver.refresh()

        # 刷新之后，父节点定位失效，重新定位
        # 不刷新无法更新审核状态（开发实现如此）

        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')
        # 列表页的审核状态
        audit_status = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr/td[12]').text

        violations_reason = table.find_element(By.XPATH,
                                               '//*[@class="table table-hover grid-table"]/tbody/tr/td[14]').text
        # 列表页的审核方式
        audit_handle_method = table.find_element(By.XPATH,
                                                 '//*[@class="table table-hover grid-table"]/tbody/tr/td[15]').text
        audit_message = table.find_element(By.XPATH,
                                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[16]').text

        check.equal(audit_status, '审核通过', '判断列表中的审核状态是否正确')
        logger.info(f'审核状态：{audit_status}')

        check.equal(violations_reason, '暴力恐怖', '判断列表中的违规原因是否正确')
        logger.info(f'违规原因：{violations_reason}')

        check.equal(audit_handle_method, '禁言1小时', '判断列表中的处理方式是否正确')
        logger.info(f'处理方式{audit_handle_method}')

        check.equal(audit_message, '', '判断列表中的备注是否正确')
        logger.info(f'备注{audit_message}')

        check_exist_punish(driver, data_key)
        logger.info("清理举报数据成功")

    @log_decorator
    @allure.title('举报信息审核通过_封号1小时')
    def test_boss_report_pass_silence_hours(self, add_report_requests):
        # 按id筛选举报列表页面
        driver.get(f'https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id={add_report_requests}')

        """ 
        driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/list?report_id=115')"""

        # 定位到table表格
        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')

        # 筛选后的举报列表，只有一条数据
        tr = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr')

        data_key = tr.get_attribute('data-key')

        # 打开审核页面
        table.find_element(By.XPATH,
                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[11]/span/a').click()
        time.sleep(1)

        # 点击审核通过
        table.find_element(By.XPATH,
                           '//*[@class="box-body no-padding"]/table/tbody/tr[1]/th/div/span/label[1]').click()

        # 定位到处理方式下拉框
        select = table.find_element(By.XPATH,
                                    '//*[@class="box-body no-padding"]/table/tbody/tr[3]/th/div/span[1]/select')
        # 选择封号
        Select(select).select_by_value('is_forbid_login')

        # 输入框
        input_box = table.find_element(By.XPATH,
                                       '//*[@class="box-body no-padding"]/table/tbody/tr[3]/th/div/span[2]/span[1]/input')
        # 全选删除后，输入1
        input_box.send_keys(Keys.CONTROL + 'a')
        input_box.send_keys(Keys.BACKSPACE)
        input_box.send_keys(1)

        # 点击确定按钮
        table.find_element(By.XPATH, '//*[@class="clearfix"]/div/a').click()

        # alert弹窗有延迟
        time.sleep(1)

        # 处理alert弹窗
        alert = driver.switch_to.alert
        alert.accept()

        driver.refresh()

        # 刷新之后，使用的父节点定位失效，重新定位
        # 不刷新无法更新审核状态（开发实现如此）

        table = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')
        # 列表页的审核状态
        audit_status = table.find_element(By.XPATH, '//*[@class="table table-hover grid-table"]/tbody/tr/td[12]').text

        violations_reason = table.find_element(By.XPATH,
                                               '//*[@class="table table-hover grid-table"]/tbody/tr/td[14]').text
        # 列表页的审核方式
        audit_handle_method = table.find_element(By.XPATH,
                                                 '//*[@class="table table-hover grid-table"]/tbody/tr/td[15]').text
        audit_message = table.find_element(By.XPATH,
                                           '//*[@class="table table-hover grid-table"]/tbody/tr/td[16]').text

        check.equal(audit_status, '审核通过', '判断列表中的审核状态是否正确')
        logger.info(f'审核状态：{audit_status}')

        check.equal(violations_reason, '暴力恐怖', '判断列表中的违规原因是否正确')
        logger.info(f'违规原因：{violations_reason}')

        check.equal(audit_handle_method, '封号1小时', '判断列表中的处理方式是否正确')
        logger.info(f'处理方式{audit_handle_method}')

        check.equal(audit_message, '', '判断列表中的备注是否正确')
        logger.info(f'备注{audit_message}')

        check_exist_punish(driver, data_key)
        logger.info("清理举报数据成功")
