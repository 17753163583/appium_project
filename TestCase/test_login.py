import time

import pytest_check as check
from loguru import logger

from Common.connect_device import connect_device
from Common.find_element import find_element_wrap
from Common.logger import log_decorator


@log_decorator
def test_login_onelap():
    driver = connect_device()
    logger.info("连接设备成功")
    # 首次打开app
    # find_element(driver, 'id', "com.onelap.bls.dear:id/tv_agree_privacy_dialog").click()
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/btn_login_index').click()
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/et_username_login').send_keys('17753163583')
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/et_password_login').send_keys('zhang107.')
    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/btn_check_out_login').click()

    find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/btn_login_login').click()
    # 首次打开app
    # find_element(driver, 'id', 'com.onelap.bls.dear:id/tv_agree_privacy_dialog').click()
    logger.info('登录完成')
    time.sleep(2)

    get_app_name = find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/tv_app_name_main_fragment')
    # 首次打开app
    # safe_dialog = find_element(driver, 'id', 'com.onelap.bls.dear:id/tv_confirm_common_dialog').click()
    if check.equal(get_app_name.text, '顽鹿运动（预发布服）'):
        logger.info("home_app_name断言成功")
    else:
        logger.error("home_app_name断言失败")
