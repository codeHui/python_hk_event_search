import requests
from datetime import datetime, timedelta
from common_utils import CommonUtils
import time

# the original event website is https://event.hkbu.edu.hk/?locale=en&date=2024-12-21&duration=week&view=grid

def fetch_events(title_filter_words):
    base_url = "https://event.hkbu.edu.hk/api/events.php"
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "authority": "event.hkbu.edu.hk",
        "method": "POST",
        "path": "/api/events.php",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "origin": "https://event.hkbu.edu.hk",
        "referer": "https://event.hkbu.edu.hk/?locale=en&date=2024-12-21&duration=week&view=grid",
    })

    # Keep track of printed titles
    printed_titles = set()

    # Prepare 6 consecutive weeks starting from the current week
    today = datetime.now()
    # Calculate offset so that weeks start on Sunday
    offset = (today.weekday() + 1) % 7
    start_of_week = datetime(today.year, today.month, today.day) - timedelta(days=offset)

    weeks = []
    for i in range(5):
        week_start = start_of_week + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        weeks.append((week_start, week_end))

    for i, (start_date, end_date) in enumerate(weeks):
        time.sleep(1)  # Pause for 1 second between iterations
        
        if i == 0:
            print("    ===== HKBU This Week =====")
        else:
            print(f"    ===== HKBU Next {i} Week =====")

        body = {
            "orderBy": "date_from",
            "query": {
                "date_from": {"$lte": start_date.strftime("%Y-%m-%d")},
                "date_to": {"$gte": end_date.strftime("%Y-%m-%d")}
            }
        }
        response = session.post(base_url, json=body)
        if response.status_code == 200:
            for event in response.json():
                date_from = event.get("date_from", "")
                date_to = event.get("date_to", "")
                time_from = event.get("time_from", "")
                time_to = event.get("time_to", "")
                if not date_from:
                    continue

                start_hour = int(time_from) if time_from.isdigit() else 0
                end_hour = int(time_to) if time_to.isdigit() else 0
                start_dt = datetime.strptime(date_from, "%Y-%m-%d") + timedelta(hours=start_hour)
                end_dt = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(hours=end_hour)

                title_en = event.get("title_en", "")
                title_tc = event.get("title_tc", "")

                if any(sub.lower() in title_en.lower() for sub in title_filter_words):
                    continue
                if any(sub.lower() in title_tc.lower() for sub in title_filter_words):
                    continue

                if CommonUtils.is_period_after_work(start_dt, end_dt):
                    # Skip if already printed
                    if title_en in printed_titles:
                        continue
                    printed_titles.add(title_en)

                    day_of_week_from = start_dt.strftime("%A")
                    day_of_week_to = end_dt.strftime("%A")
                    if date_to == date_from:
                        date_display = f"{date_from} ({day_of_week_from})"
                    else:
                        date_display = f"{date_from} ({day_of_week_to}) - {date_to} ({day_of_week_to})"

                    print(f"Title: {title_en}")
                    if title_tc and title_tc != title_en:
                        print(f"Title Chinese: {title_tc}")
                    print(f"Date: {date_display}")
                    print(f"Time: {time_from}:00 - {time_to}:00" if time_from else "Time: check the url")
                    print(f"Venue: {event.get('location_other_en', '')}")
                    print(f"URL: {event.get('website', '')}")
                    print("-" * 40)
        else:
            print(f"Request error: {response.status_code}")

# ...existing code...
if __name__ == "__main__":
    from main import title_filter_config
    fetch_events(title_filter_config["hkbu"])
