import requests
from datetime import datetime, time, timedelta
from bs4 import BeautifulSoup

# URL and parameters
url = "https://www.polyu.edu.hk/en/api/sitecore/calendar/search"
params = {
    "id": "F45B40DE7F3F4AFA9B2D02B1D824C1E0",
    # "m": "12",
    "y": "2025",
    # type conference / lecture
    "t": "160E32E12F4348DC8A3FAED76003F4B5"
}

# Send GET request
response = requests.get(url, params=params)
data = response.json()
# print(data)

def is_event_on_weekend_or_after_hours(event_start,event_end):
    # return ture if there is Saturday or Sunday in between event_start and event_end
    current_date = event_start
    while current_date <= event_end:
        if current_date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
            return True
        current_date += timedelta(days=1)

    # return true if event_start is after 18:30 on a weekday
    return event_start.time() >= time(18, 20)

# Iterate over events
for event in data.get("events", []):
    # print(event)
    event_start_str = event.get("eventStartDate")
    event_end_str = event.get("eventEndDate")
    title = event.get("title")
    if not event_start_str:
        continue

    event_start = datetime.fromisoformat(event_start_str)
    event_end = datetime.fromisoformat(event_end_str)

    # Check if event is on weekend or after 18:30 on a weekday
    if True:
    # if is_event_on_weekend_or_after_hours(event_start,event_end):
        # Parse content to get title and href
        content = event.get("content", "")
        soup = BeautifulSoup(content, "html.parser")
        a_tag = soup.find("a", href=True, title=True)
        if a_tag:
            # title = a_tag.text.strip()
            href = a_tag['href']
            print(f"Title: {title}")
            print(f"Start Date: {event_start.strftime('%Y-%m-%d %H:%M:%S')}, {event_start.strftime('%A')}")
            print(f"End Date  : {event_end.strftime('%Y-%m-%d %H:%M:%S')}, {event_end.strftime('%A')}")
            print(f"URL: {href}\n")



