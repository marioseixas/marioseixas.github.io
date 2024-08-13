import requests
from requests.auth import HTTPDigestAuth
import json
from icalendar import Calendar

url = "https://dav.heydola.com/dav.php/calendars/py28wj81/default/?export"
username = "py28wj81"
password = "20287290"

response = requests.get(url, auth=HTTPDigestAuth(username, password))

if response.status_code == 200:
    print("Access successful!")
    calendar = Calendar.from_ical(response.text)
    events = []

    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {
                "title": str(component.get('SUMMARY')),
                "start": component.get('DTSTART').dt.isoformat(),
                "end": component.get('DTEND').dt.isoformat(),
            }
            events.append(event)

    with open("https://github.com/marioseixas/marioseixas.github.io/blob/main/assets/data/events.json", "w") as f:
        json.dump(events, f)
else:
    print(f"Failed to access. Status code: {response.status_code}")
    print(response.text)
