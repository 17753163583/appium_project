import requests
from bs4 import BeautifulSoup


def boss_login(url):
    session = requests.session()
    response_get = session.get(url, verify=False)

    soup = BeautifulSoup(response_get.text, 'lxml')

    # 查找_token值
    token = soup.find('input', attrs={'name': '_token'})['value']

    json_body = {
        'username': 'onelap',
        'password': 'onelap@123',
        '_token': token
    }

    # 自动携带Get方法生成的Cookies
    response = session.post(url, data=json_body)
