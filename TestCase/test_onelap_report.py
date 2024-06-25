import time

import pytest_check as check
from selenium.webdriver import ActionChains

from Common.connect_device import connect_device_later
from Common.find_element import find_element_wrap
from Common.logger import log_decorator


class TestOnelap:

    @log_decorator
    def test_report(self, login_onelap):
        driver = connect_device_later()
        actions = ActionChains(driver)

        # 初次登录时使用
        # find_element_wrap(driver, 'id', "com.android.packageinstaller:id/permission_allow_button").click()

        find_element_wrap(driver, 'id', "com.onelap.bls.dear:id/include_planet_bottom_navigation").click()

        # 关闭第一次打开路线页的安全提示(登录完成后会切换页面，容易造成异常)
        find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/tv_confirm_common_dialog').click()

        # 打开搜索框
        find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/tv_search').click()
        # 搜索测试路线
        find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/key_input').send_keys(304)
        driver.keyevent(66)

        find_element_wrap(driver, 'xpath',
                          '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.onelap.bls.dear:id/rv_route_list"]/android.view.ViewGroup').click()

        time.sleep(5)

        find_element_wrap(driver, 'xpath', '//android.view.View[@text="骑友评论"]').click()
        content = find_element_wrap(driver, 'xpath',
                                    '//android.view.View[@resource-id="content-wrap"]/android.view.View[3]/android.view.View[2]/android.view.View/android.view.View[2]/android.view.View[3]')

        actions.click_and_hold(content).pause(2).release().perform()

        find_element_wrap(driver, 'xpath', '//android.view.View[@text="举报"]').click()
        time.sleep(1)

        find_element_wrap(driver, 'xpath', '//android.widget.TextView[@text="低俗色情"]').click()
        find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/tv_content').send_keys('测试')

        status = find_element_wrap(driver, 'id', 'com.onelap.bls.dear:id/btn_submit')
        check.is_true(status)

        # 使用是否存在来捕获toast，是否可见无法捕获toast
        # WebDriverWait(driver, 10, 0.25).until(ec.presence_of_element_located(('xpath', '//android.widget.Toast[@text="你的举报我们已成功收到，会尽快核实处理"]')))
        # print("测试成功。。。。。")
