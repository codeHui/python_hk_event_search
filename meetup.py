import requests
from bs4 import BeautifulSoup
from datetime import datetime
from common_utils import CommonUtils
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_events(title_filter_words=[]):
    # categoryId=546 is for "Tech" events
    url = "https://www.meetup.com/find/?source=EVENTS&eventType=inPerson&sortField=DATETIME&location=hk--Kowloon&categoryId=546"
    
    driver = None
    try:
        # 設置 Chrome 選項
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式，不顯示瀏覽器
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # 初始化 Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # 訪問網址
        print("Loading the page with Selenium...")
        driver.get(url)
        
        # 等待頁面加載 - 增加等待時間以確保動態內容加載完成
        print("Waiting for dynamic content to load...")
        wait = WebDriverWait(driver, 5)  # 等待最多15秒
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "max-w-narrow")))

        # 再等待一點時間確保所有事件都已加載
        time.sleep(5)
        
        # 獲取完整的 HTML
        page_source = driver.page_source
        
    except Exception as e:
        print(f"Selenium error: {e}")
        import traceback
        traceback.print_exc()
        page_source = None
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing driver: {e}")

    if not page_source:
        print("No page source to parse. Exiting.")
        return

    # 用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # 查找事件列表 div
    event_list_div = soup.find('div', class_="max-w-narrow")
    if not event_list_div or not hasattr(event_list_div, 'find_all'):
        print("Could not find event list div or it is not a valid tag")
        return
    
    # 查找所有事件 div
    event_divs = event_list_div.find_all('div', class_="w-full overflow-hidden")
    
    for event_div in event_divs:
        # if contains "event series", then skip
        if "event series" in event_div.text.lower():
            continue
        # Get the 'a' tag inside the event div
        a_tag = event_div.find('a')
        if not a_tag:
            continue
        
        # Get the time
        time_element = a_tag.find('time')
        event_time = time_element.text.strip() if time_element else "Time not found"
        
        # Get the title
        title_element = a_tag.find('h2')
        title = title_element.text.strip() if title_element else "Title not found"
        
        # Filter out events with titles containing any of the filter substrings
        if any(keyword.lower() in title.lower() for keyword in title_filter_words):
            continue
        
        # Parse time string to datetime object
        try:
            # Example format: "Wed, Apr 23 · 2:00 PM HKT"
            # First split by "·" to separate date and time
            date_time_parts = event_time.split('·')
            if len(date_time_parts) >= 2:
                date_part = date_time_parts[0].strip()  # "Wed, Apr 23"
                time_part = date_time_parts[1].strip().split(' HKT')[0].strip()  # "2:00 PM"
                
                # Parse the date and time
                # Add current year if not present
                if not any(char.isdigit() and len(char) == 4 for char in date_part.split()):
                    current_year = datetime.now().year
                    date_part = f"{date_part} {current_year}"
                
                # Combine date and time for parsing
                date_time_str = f"{date_part} {time_part}"
                event_start = datetime.strptime(date_time_str, "%a, %b %d %Y %I:%M %p")
                
                # Check if event is after work hours or on weekend
                if not CommonUtils.is_time_after_work(event_start):
                    continue
            else:
                # If we can't parse the time properly, still show the event
                pass
        except Exception as e:
            print(f"Time parsing error for '{event_time}': {e}")
        
        # Get the event URL
        event_url = a_tag.get('href', '')
        
        print(f"Time: {event_time}")
        print(f"Title: {title}")
        if event_url:
            print(f"URL: {event_url}")
        print("-" * 40)
        
if __name__ == "__main__":
    from main import title_filter_config
    fetch_events(title_filter_config["meetup"])
