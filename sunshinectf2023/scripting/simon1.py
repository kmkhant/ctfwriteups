import requests

url = "https://simon1.web.2023.sunshinectf.games/"
session = "60c1f27c-d857-47e8-8ec9-ec022b7511f1"
frequencies = requests.get(url + "frequencies", verify=False)

frequencies = frequencies.content.strip().decode()

print(frequencies)

resp = requests.post(url=url + "fetch", data=frequencies, verify=False)

print(resp.content)
