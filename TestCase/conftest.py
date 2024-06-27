import json
import time

import pytest
import pytest_check as check
import requests
from loguru import logger
from selenium.webdriver.common.by import By

from Common.connect_device import connect_device_first
from Common.find_element import find_element_wrap
from Common.get_boss_authorization import get_boss_authorization
from Common.logger import log_decorator


@log_decorator
@pytest.fixture(scope='session')
def login_onelap():
    driver = connect_device_first()
    logger.info("连接设备成功")
    # 首次打开app
    find_element_wrap(driver, 'id', "com.onelap.bls.dear:id/tv_agree_privacy_dialog").click()
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/btn_login_index').click()
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/et_username_login').send_keys('17753163583')
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/et_password_login').send_keys('zhang107.')
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/btn_check_out_login').click()

    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/btn_login_login').click()
    # 首次打开app
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/tv_agree_privacy_dialog').click()
    logger.info('登录完成')
    time.sleep(2)

    get_app_name = find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/tv_app_name_main_fragment')
    # 首次打开app
    # find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/tv_confirm_common_dialog').click()
    if check.equal(get_app_name.text, '顽鹿运动（预发布服）'):
        logger.info(f"{get_app_name.text}断言成功，登录成功")
    else:
        logger.error(f"{get_app_name.text}断言失败，登录失败")


@log_decorator
@pytest.fixture(scope='function')
def get_boss_cookies(driver):
    driver.get("https://boss-informal.rfsvr.net/auth/login")

    logger.info("输入用户名和密码")

    time.sleep(15)

    dict_cookies = driver.get_cookies()
    logger.info("获取cookies成功")
    json_cookies = json.dumps(dict_cookies)
    # print(json_cookies)
    with open('../TestData/login_cookies.json', 'w') as f:
        f.write(json_cookies)
        logger.info("保存cookies到本地")
    logger.info("删除cookies成功")
    driver.delete_all_cookies()


@log_decorator
@pytest.fixture(scope='function')
def add_report_requests():
    # 创建一条举报数据
    url = 'https://rfs-fitness-informal.rfsvr.net/indoor/api/user/report'

    # 获取boss后台接口的访问密钥
    token = get_boss_authorization()
    headers = {'Authorization': token, 'UserId': '238492'}

    data = {"desc": "脚本测试", "source_id": 698, "reason_id": 3, "source_type": 1}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        logger.info('添加举报数据成功')
        json_response = json.loads(response.text)
        report_id = json_response['data']['report_id']

        return report_id
    else:
        logger.info('添加举报数据失败')


@log_decorator
@pytest.fixture(scope='function')
def add_report_requests_test_yield(driver, data_key):
    # 创建一条举报数据
    url = 'https://rfs-fitness-informal.rfsvr.net/indoor/api/user/report'

    # 获取boss后台接口的访问密钥
    token = get_boss_authorization()
    headers = {'Authorization': token, 'UserId': '238492'}

    data = {"desc": "脚本测试", "source_id": 698, "reason_id": 3, "source_type": 1}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        logger.info('添加举报数据成功')
        json_response = json.loads(response.text)
        report_id = json_response['data']['report_id']
        yield report_id


        driver.get('https://boss-informal.rfsvr.net/admin/wl/social/user/report/handle')
        tbody = find_element_wrap(driver, 'xpath', '//*[@class="table table-hover grid-table"]/tbody')
        target_tr = tbody.find_element(By.XPATH, f'//*[@data-key="{data_key}"]')

        data_key = (target_tr.get_attribute('data-key'))
        print(data_key)
        # 展开撤销
        target_tr.find_element(By.XPATH, f'//*[@data-key="{data_key}"]/td[12]/div/a').click()

        # 展开表单后，xpath路径中div元素的class属性发生变化
        # 点击撤销按钮
        target_tr.find_element(By.XPATH, f'//*[@data-key="{data_key}"]/td[12]/div/ul/li/a').click()
        print('完成')

    else:
        logger.info('添加举报数据失败')
