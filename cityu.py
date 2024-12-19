# cityu.py

# Import necessary libraries
from requests_html import HTMLSession
from lxml_html_clean import Cleaner
from bs4 import BeautifulSoup
from datetime import datetime
from common_utils import CommonUtils

# URL to scrape
url = "https://www.cityu.edu.hk/calendar/event"

def fetch_events():
    session = HTMLSession()
    response = session.get(url)
    
    # Directly parse the HTML content without rendering JavaScript
    soup = BeautifulSoup(response.content, 'html.parser')
    events = soup.find_all('div', class_='views-row')

    for event in events:
        # 10 Jan 2025 (Fri) 3:00 PM - 4:00 PM
        date = event.find('div', class_='event-period-date').get_text(strip=True)
        # 3:00 PM - 4:00 PM
        time = event.find('div', class_='event-period-time').get_text(strip=True)
        categories = event.find('div', class_='event-categories').get_text(strip=True)
        title = event.find('div', class_='event-title').get_text(strip=True)
        venue = event.find('div', class_='event-venue').get_text(strip=True)
        urlHerf = event.find('div', class_='event-title').find('a')['href']

        # Extract the start time from the time string
        start_time = time.split('-')[0].strip()
        # Combine date and start time strings and convert to a datetime object
        event_datetime_str = f"{date.split(' (')[0]} {start_time}"
        event_datetime = datetime.strptime(event_datetime_str, "%d %b %Y %I:%M %p")

        # Check if the event time is after work hours
        if CommonUtils.is_time_after_work(event_datetime):
            print(f"Title: {title}")
            print(f"Date: {date}")
            print(f"Time: {time}")
            # print(f"Categories: {categories}")
            print(f"Venue: {venue}")
            print(f"URL: {urlHerf}")
            print("-" * 40)

if __name__ == "__main__": 
    fetch_events()
