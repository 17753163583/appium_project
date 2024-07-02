import requests


def get_onelap_authorization():
    url = 'https://rfs-fitness-informal.rfsvr.net/api/account/v1/login'
    body = {"account": "17753163583", "password": "dc158e485dba3cb7a6cfc9063568ac9e"}

    response = requests.post(url, data=body)
    token = response.json()['data']['token']
    return token


if __name__ == '__main__':
    get_onelap_authorization()
