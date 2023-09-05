import requests

# api_key = "F558CCE032B1433B9B531557812B33D7"
# header = {"Authorization": f"Bearer {api_key}"}
params = {"apikey": 'B508534ED20348F090B4D0AD637D3660'}
# response = requests.get(url="http://10.114.58.251:5000/api/connection",params = params)
# cmd = {
#     "profile": {
#         "id": "some_profile3",
#         "name": "Some profile 3",
#         "model": "Some cool model 3"
#     }
# }

cmd = {
    "command":"FORCE_MOVE",
    "STEPPER": 'steper_y',
    "DISTANCE": '20',
    "VELOCITY": '20'
}
#request = requests.post(url="http://10.114.56.121/api/printer/command", params=params, json=cmd)
# data = request.json()['job']

get_requests = requests.get(url="http://10.114.56.121/api/printer/chamber",params=params)

get_requests.raise_for_status()
print(get_requests.text)
