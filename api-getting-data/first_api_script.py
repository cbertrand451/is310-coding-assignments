import requests

# url = 'https://the-one-api.dev/v2/book'

# response = requests.get(url)

# print(response.status_code)

# print(response.json())

url = 'https://the-one-api.dev/v2/character'
response = requests.get(url)
print(response.status_code)