import requests

url = 'http://rfs-fitness-informal.rfsvr.net/api/account/v1/login'
data = {
    "account": "13001723386",
    "password": "dc158e485dba3cb7a6cfc9063568ac9e"
}

r = requests.post(url, data=data)
print(r.text)
