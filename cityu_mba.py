import requests
from bs4 import BeautifulSoup
from datetime import datetime
from common_utils import CommonUtils

def fetch_events():
    url = "https://mba.cb.cityu.edu.hk/about/upcoming-events"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request error: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, "html.parser")
    event_boxes = soup.find_all("div", class_="view-content-list-grid-box")
    for box in event_boxes:
        # 日期與時間
        date_time_tag = box.find("div", class_="date-time d-flex")
        if date_time_tag:
            import re
            date_time_text = date_time_tag.get_text(" ", strip=True)
            date_time_text = re.sub(r'\s+', ' ', date_time_text).strip()
            date_time_text = date_time_text.replace('，', ',')
            
            # 用正則提取日期和時間
            m = re.match(r"([0-9]{1,2} [A-Za-z]+ [0-9]{4}) ?(?:\([^)]+\))?[, ]*([0-9:apmAPM\-–]+)", date_time_text)
            if m:
                date_str = m.group(1).strip()
                time_str = m.group(2).strip()
            else:
                print(f"cityu mba skip: 無法解析日期時間: '{date_time_text}'")
                continue
        else:
            print("cityu mba skip: 無法找到日期時間標籤")
            continue
        # 標題
        title_tag = box.find("div", class_="title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        # type/venue
        type_tag = box.find("div", class_="venue d-flex")
        type_str = type_tag.get_text(strip=True) if type_tag else ""
        if type_str == "Online via Zoom":
            continue
        # 連結
        link_tag = box.find("a", href=True)
        url_event = link_tag['href'] if link_tag else url
        # 組合時間過濾
        try:
            # 例：7:00-8:30pm 或 7:00pm-8:30pm
            import re
            time_range = time_str.replace('–', '-').replace(' ', '')
            m = re.match(r'(\d{1,2}:\d{2})(am|pm)?-(\d{1,2}:\d{2})(am|pm)', time_range, re.IGNORECASE)
            if m:
                start_time = m.group(1)
                start_ampm = m.group(2)
                end_ampm = m.group(4)
                # 如果開始時間沒 AM/PM，補上結束時間的 AM/PM
                if not start_ampm:
                    start_ampm = end_ampm
                dt_str = f"{date_str} {start_time}{start_ampm}"
            else:
                # fallback: 只取第一段
                dt_str = f"{date_str} {time_str.split('-')[0].split('–')[0].strip()}"
            event_dt = datetime.strptime(dt_str, "%d %B %Y %I:%M%p")
        except Exception:
            print(f"error cityu mba Error parsing date: {date_str}，{time_str}")
            continue
        if CommonUtils.is_time_after_work(event_dt):
            print(f"Title: {title}")
            print(f"Date: {date_str}")
            print(f"Time: {time_str}")
            print(f"Type: {type_str}")
            print(f"URL: {url_event}")
            print("-" * 40)

if __name__ == "__main__":
    fetch_events()
