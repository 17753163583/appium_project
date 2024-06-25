from appium import webdriver
from appium.options.android import UiAutomator2Options


def connect_device_first():
    capabilities = dict(
        platformName='Android',
        platformVersion='12',
        automationName='uiautomator2',
        deviceName='127.0.0.1:16384',
        appPackage='com.onelap.bls.dear',
        appActivity='com.onelap.bls.dear.activity.riding_splash.SplashActivity',

        # 设置为False，对app重置全部数据（调试登录可用）
        noReset=False
    )

    # 创建driver对象
    appium_server_url = 'http://127.0.0.1:4723'
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    return driver


def connect_device_later():
    capabilities = dict(
        platformName='Android',
        platformVersion='12',
        automationName='uiautomator2',
        deviceName='127.0.0.1:16384',

        # 设置为False，对app重置全部数据（调试登录可用）
        noReset=True
    )

    # 创建driver对象
    appium_server_url = 'http://127.0.0.1:4723'
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    return driver
