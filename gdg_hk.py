import requests
from datetime import datetime
from common_utils import CommonUtils

def fetch_events():
    url = "https://gdg.community.dev/api/event_slim/for_chapter/660/?page_size=4&status=Live&include_cohosted_events=true&visible_on_parent_chapter_only=true&order=start_date&fields=title,start_date,event_type_title,cropped_picture_url,cropped_banner_url,url,cohost_registration_url,description,description_short&page=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request error: {response.status_code}")
        return
    data = response.json()
    events = data.get("results", [])
    for event in events:
        title = event.get("title", "")
        start_date_str = event.get("start_date", "")
        event_type = event.get("event_type_title", "")
        url_event = event.get("url", "")
        desc_short = event.get("description_short", "")
        # Parse start date
        try:
            event_start = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
        except Exception as e:
            print(f"Error parsing date: {start_date_str}, {e}")
            continue
        # the time here is not aligned with the detail page
        # if CommonUtils.is_time_after_work(event_start):
        print(f"Title: {title}")
        # print(f"Type: {event_type}")
        # print(f"Start: {event_start.strftime('%Y-%m-%d %H:%M:%S')}, {event_start.strftime('%A')}")
        print(f"URL: {url_event}")
        if desc_short:
            print(f"Description: {desc_short}")
        print("-" * 40)

if __name__ == "__main__":
    fetch_events()
