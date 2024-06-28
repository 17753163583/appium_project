import json
import time

import pytest
import requests
from loguru import logger

from Common.get_boss_authorization import get_boss_authorization
from Common.logger import log_decorator


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


@pytest.fixture(scope='session')
@log_decorator
def create_data_key_dict():
    json_data_dict = {'is_forbid_speak': [], 'is_forbid_login': []}
    data_key_json_file_name = '../TestData/data_key_dict.json'
    with open(data_key_json_file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data_dict))
        logger.info("惩罚信息json文件创建成功")


def report_not_pass_csrf_token():
    csrf_token = get_boss_authorization()
