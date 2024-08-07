import requests
from requests.auth import HTTPDigestAuth

# Replace with your actual URL, username, and password
url = "https://dav.heydola.com/dav.php/calendars/py28wj81/default/?export"
username = "py28wj81"
password = "20287290"

response = requests.get(url, auth=HTTPDigestAuth(username, password))

if response.status_code == 200:
    print("Access successful!")
    print(response.content.decode('utf-8'))
else:
    print(f"Failed to access. Status code: {response.status_code}")
    print(response.text)
