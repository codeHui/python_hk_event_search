import requests
import json
from datetime import datetime, timedelta, time
import time as t

url = "https://www.eventbrite.hk/api/v3/destination/search/"

skip_keywords = ["Weekly Social HackJam","AIA", "Eats Out", "Drink","瑜伽","Meditation","展覽","Testing","NETMHK","Live Music","創意工作坊","SALSA FEVER","護手霜","Fringe Club","Kizomba"]
categoryArr = [
    # Business
    # "EventbriteCategory/101",
    # Health
    # "EventbriteCategory/107",
    # Charity & Causes
    # "EventbriteCategory/111",
    # Community
    # "EventbriteCategory/113",
    # Family & Education
    # "EventbriteCategory/115",
    # Fashion
    # "EventbriteCategory/106",
    # Film & Media
    # "EventbriteCategory/104",
    # Hobbies
    # "EventbriteCategory/119",
    # Home & Lifestyle
    # "EventbriteCategory/117",
    # Performing & Visual Arts
    # "EventbriteCategory/105",
    # Government
    # "EventbriteCategory/112",
    # Spirituality
    # "EventbriteCategory/114",
    # School Activities
    # "EventbriteCategory/120",
    # Science & Tech
    # "EventbriteCategory/102",
    # Holidays
    # "EventbriteCategory/116",
    # Other
    "EventbriteCategory/199",
]


def is_event_on_weekend_or_after_hours(start_date_str, end_date_str, start_time_str):
    # Combine start date and time
    start_datetime = datetime.strptime(
        f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M"
    )
    # Parse end date
    end_datetime = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Check for weekend days between start and end dates
    current_date = start_datetime.date()
    end_date = end_datetime.date()
    while current_date <= end_date:
        if current_date.weekday() >= 5:  # Saturday or Sunday
            return True
        current_date += timedelta(days=1)

    # Check if event starts after 18:20 on a weekday
    if start_datetime.time() >= time(18, 20):
        return True
    return False


# for Category
for category in categoryArr:
    payload = json.dumps(
        {
            "event_search": {
                "dates": ["current_future", "this_month"],
                "dedup": True,
                "places": ["85671791"],
                "price": "free",
                "page": 1,
                "page_size": 50,
                "online_events_only": False,
                "tags": [category],
            },
            "expand.destination_event": [
                "primary_venue",
                "image",
                "ticket_availability",
                "saves",
                "event_sales_status",
                "primary_organizer",
                "public_collections",
            ],
            "debug_experiment_overrides": {"search_exp_4": "D"},
            "browse_surface": "search",
        }
    )
    headers = {
        "Referer": "https://www.eventbrite.hk/d/hong-kong-sar--yau-tsim-mong--85671791/free--events--this-month/?page=1",
        "Cookie": 'csrftoken=82bcd3cca4fc41d78448c0d4b39954b1; django_timezone=Asia/Hong_Kong; _dd_s=rum=0&expire=1733738307710; _ga_TQVES5V6SH=GS1.1.1733737307.1.1.1733737374.60.0.0; _ga=GA1.1.1793637248.1733737307; stableId=fa11db88-ff08-45ea-9085-e6ae81f9cab0; SP=AGQgbblJVjRB13eokeMHp4d0Vlg0VTQ0LPgpS2rJmIkwF-nEaYinRxm68DOBfwwX2TtT-1AhzTsdgcSQi0wod4pONb46CGwhyD_3HqRAtrw3pF5RfZvXY_Z_n1BLiVZNwLVnQ3SH9-HYOzUOyAyniIZcGE-Q4kbDAU9_90OpNNlqQfFzKE994Dgfx2QHY6ZKdIXoDB239eLSn1tS71LnyKY8vg2F0Wbr5jooS0e0Rb1HlbxA8RYYuqk; guest=identifier%3D607f6067-5966-42ac-bd7d-b234c9172712%26a%3D136b%26s%3D6edc31a0c3f92451078e89fb31b8950193d17afbfce7965318a93edb55c0c723; G=v%3D2%26i%3D607f6067-5966-42ac-bd7d-b234c9172712%26a%3D136b%26s%3Db5a9d38ac5b56544e62574ec2723786388dda662; SS=AE3DLHSvnUDAw8Mpt7Iy7TdUv1GLpfVm8g; eblang=lo%3Den_HK%26la%3Den-gb; AS=f9d478cd-9530-4b7b-8b1b-1099546b66de; location=%7B%22current_place_parent%22%3A%20%22Hong%20Kong%20S.A.R.%22%2C%20%22place_type%22%3A%20%22region%22%2C%20%22current_place%22%3A%20%22Yau%20Tsim%20Mong%22%2C%20%22latitude%22%3A%2022.2908%2C%20%22country%22%3A%20%22Hong%20Kong%20S.A.R.%22%2C%20%22place_id%22%3A%20%2285671791%22%2C%20%22slug%22%3A%20%22hong-kong-sar--yau-tsim-mong--85671791%22%2C%20%22longitude%22%3A%20114.1501%7D; tcm={"purposes":{"Advertising":"Auto","Functional":"Auto","Analytics":"Auto","SaleOfInfo":false},"timestamp":"2024-12-09T09:42:29.629Z","confirmed":false,"prompted":false,"updated":false}; _gcl_au=1.1.1415530939.1733737351; location={%22current_place_parent%22:%22Hong%20Kong%20S.A.R.%22%2C%22place_type%22:%22region%22%2C%22current_place%22:%22Yau%20Tsim%20Mong%22%2C%22latitude%22:22.2908%2C%22country%22:%22Hong%20Kong%20S.A.R.%22%2C%22place_id%22:%2285671791%22%2C%22slug%22:%22hong-kong-sar--yau-tsim-mong--85671791%22%2C%22longitude%22:114.1501}; AS=f9d478cd-9530-4b7b-8b1b-1099546b66de; G=v%3D2%26i%3Dfc9d2394-c53e-49f4-97aa-936b18f0907f%26a%3D136b%26s%3Df75b0aec04a017c9ba84244655321c4e67096762; SP=AGQgbbn2zeJnbLjRF7CFUirfmLF3HAajT3sJPvIhZ3ktlg8P_zuQV4uhd4H8jystLUB1hqSwGNOrX1n97AvgPZyLdHZutW-7SxhIesYOJijQ0KhlwcjLEHaasWir-p0N8RK0NUJdwgP3faIHiCu9HXbOXPwYDNNaZxxUv4qg0R8EBrhWmAaYz8p-0dOGEc6Vw_ZtRe0X3EAdyc5yN-6EIgZleWYILTYJFzyFgbBPkZlyxMgJJYM6tCQ; SS=AE3DLHSwRjQ1y1KR0WgDndTX0lr44R9jGw; eblang=lo%3Den_HK%26la%3Den-gb; guest=identifier%3Dfc9d2394-c53e-49f4-97aa-936b18f0907f%26a%3D136b%26s%3Dc3395e7b9f940929bad181604e85ef78b4b2262ed67a4478412d9c676e2a37c2; mgref=typeins; mgrefby=; stableId=fa11db88-ff08-45ea-9085-e6ae81f9cab0',
        "X-CSRFToken": "82bcd3cca4fc41d78448c0d4b39954b1",
        "Content-Type": "application/json",
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Response Text:\n{response.status_code}")
            # print(f"Response Text:\n{response.text}")
            continue
        data = response.json()
        results = data["events"]["results"]
        print(f"{len(results)} {category}\n\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        t.sleep(20)
        continue

    # Iterate over results
    for event in results:
        is_online_event = event.get("is_online_event")

        start_date = event.get("start_date")
        end_date = event.get("end_date")
        start_time = event.get("start_time")
        end_time = event.get("end_time")
        title = event.get("name")
        url = event.get("url")
        localized_address_display = event.get("primary_venue").get("address").get("localized_address_display")

        event_start = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        event_end = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")


        if not is_online_event:
            # if title contains "AIA" "Eats Out", then skip
            if any(keyword in title for keyword in skip_keywords):
                continue
            if is_event_on_weekend_or_after_hours(start_date, end_date, start_time):
                print(f"Title: {title}")
                print(
                    f"Start Date: {event_start.strftime('%Y-%m-%d %H:%M:%S')}, {event_start.strftime('%A')}"
                )
                print(
                    f"End Date  : {event_end.strftime('%Y-%m-%d %H:%M:%S')}, {event_end.strftime('%A')}"
                )
                print(f"URL: {localized_address_display}\n")
                print(f"URL: {url}\n")

    t.sleep(5)