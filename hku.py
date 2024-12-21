# Import necessary libraries
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
from common_utils import CommonUtils

# URL to scrape
url = "https://www.hku.hk/event/upcoming.html"

def fetch_events(title_filter_words):
    session = HTMLSession()
    response = session.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    events_table = soup.find('table', summary='a list of Upcoming Events')
    if not events_table:
        print("No events table found.")
        return
    
    events = events_table.find_all('tr')[1:]  # Skip header row

    for event in events:
        tds = event.find_all('td')
        if len(tds) < 4:
            # Not enough columns
            continue
        
        # Extract date and time
        date_time = tds[0].get_text(separator='\n', strip=True).split('\n')
        # Example: '25 Dec 2024 - 19 Jan 2025'
        date = date_time[0] if len(date_time) > 0 else ""
        # Example: '11:00-20:00'
        time = date_time[1] if len(date_time) > 1 else "00:00-00:00"
        
        # Extract start and end time
        if '-' in time:
            start_time, end_time = time.split('-', 1)
            start_time = start_time.strip()
            end_time = end_time.strip()
        else:
            start_time = time.strip()
            end_time = "00:00"
        
        # Extract start and end dates
        if ' - ' in date:
            start_date, end_date = date.split(' - ', 1)
            start_date = start_date.strip()
            end_date = end_date.strip()
        else:
            start_date = date.strip()
            end_date = start_date
        
        # Combine date and time strings
        # start_date example: "23 Dec"
        # end_date example: "23 Dec 2024"
        # event_start_str should include year: "23 Dec 2024 15:00"
        event_start_str = f"{start_date} {start_time}"
        event_end_str = f"{end_date} {end_time}"
        
        # If start_date doesn't include year, append year from end_date
        # Example: start_date '23 Dec' -> '23 Dec 2024'
        if not any(char.isdigit() for char in start_date.split()[-1]):
            # Extract year from end_date
            end_date_parts = end_date.split()
            if len(end_date_parts) >= 3 and end_date_parts[-1].isdigit():
                year = end_date_parts[-1]
                start_date += f" {year}"
                event_start_str = f"{start_date} {start_time}"
            else:
                print(f"Unable to extract year from end_date: '{end_date}' for event: '{title}'")
                continue
        
        # Initialize title to avoid UnboundLocalError
        title = ""
        
        # Extract title and URL
        title_tag = tds[3].find('a')
        if title_tag:
            title = title_tag.get_text(strip=True)
            urlHref = title_tag['href']
        else:
            urlHref = ""
        
        # Filter out events with titles containing any of the filter substrings
        if any(sub.lower() in title.lower() for sub in title_filter_words):
            continue
        
        try:
            event_start = datetime.strptime(event_start_str, "%d %b %Y %H:%M")
            event_end = datetime.strptime(event_end_str, "%d %b %Y %H:%M")
        except ValueError as e:
            print(f"Error parsing date/time for event: '{title}'. Details: {e}")
            print(f"Invalid start_str: '{event_start_str}', end_str: '{event_end_str}'")
            continue

        # Get day of the week
        day_of_week = event_start.strftime('%A')

        # Extract venue
        venue = tds[1].get_text(strip=True)
        
        # Filter out events with venue 'Zoom' or 'via Zoom' (case-insensitive)
        if venue.lower() in ["zoom", "via zoom"]:
            continue

        # Check if event is on weekend or after hours
        if CommonUtils.is_period_after_work(event_start, event_end):
            print(f"Title: {title}")
            print(f"Date: {date} ({day_of_week})")
            print(f"Time: {time}")
            print(f"Venue: {venue}")
            print(f"URL: {urlHref}")
            print("-" * 40)

# ...existing code...
if __name__ == "__main__": 
    from main import title_filter_config
    fetch_events(title_filter_config["hku"])
