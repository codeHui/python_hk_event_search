import requests
from datetime import datetime, timedelta
from common_utils import CommonUtils
import time

def fetch_events():
    url = "https://api.lu.ma/discover/get-paginated-events?discover_place_api_id=discplace-z9B5Guglh2WINA1&pagination_limit=50"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Request error: {response.status_code}")
            return
        
        data = response.json()
        events = data.get("entries", [])
        
        for event in events:
            ticket_info = event.get("ticket_info", {})
            
            # Filter for events that are free, not sold out, and not near capacity
            if ticket_info.get("is_free", False) and not ticket_info.get("is_sold_out", True) and not ticket_info.get("is_near_capacity", True):
                # Extract event details
                event_data = event.get("event", {})
                title = event_data.get("name", "")
                start_time_str = event_data.get("start_at", "")
                end_time_str = event_data.get("end_at", "")
                venue = "Unknown"
                
                # Get location information if available
                if event_data.get("geo_address_info") and event_data.get("geo_address_info").get("mode") != "obfuscated":
                    address_info = event_data.get("geo_address_info", {})
                    venue_parts = []
                    if address_info.get("address"):
                        venue_parts.append(address_info.get("address"))
                    if address_info.get("full_address"):
                        venue_parts.append(address_info.get("full_address"))
                    venue = venue_parts[0] if venue_parts else "Unknown"
                
                # Get URL for the event
                event_url = f"https://lu.ma/{event_data.get('url', '')}"
                
                # Parse event times and convert to Hong Kong time (UTC+8)
                try:
                    event_start = datetime.fromisoformat(start_time_str.replace('Z', '+00:00')) + timedelta(hours=8)
                    event_end = datetime.fromisoformat(end_time_str.replace('Z', '+00:00')) + timedelta(hours=8)
                except Exception as e:
                    print(f"Error parsing date: {start_time_str}, {e}")
                    continue
                
                # Check if event is after work hours
                if CommonUtils.is_period_after_work(event_start, event_end):
                    print(f"Title: {title}")
                    print(f"Start Date: {event_start.strftime('%Y-%m-%d %H:%M:%S')}, {event_start.strftime('%A')}")
                    print(f"End Date  : {event_end.strftime('%Y-%m-%d %H:%M:%S')}, {event_end.strftime('%A')}")
                    print(f"Venue: {venue}")
                    print(f"URL: {event_url}")
                    print("-" * 40)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_events()
