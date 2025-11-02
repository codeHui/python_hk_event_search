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
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 初始化 Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        
        # 訪問網址
        print("Loading the page with Selenium...")
        driver.get(url)
        
        # 等待頁面加載 - 增加等待時間以確保動態內容加載完成
        print("Waiting for dynamic content to load...")
        # Wait for body to be present first
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Scroll down to trigger lazy loading
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        
        # Wait for events to load - try multiple possible selectors
        print("Waiting for events to appear...")
        try:
            # Try waiting for event cards
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/events/']")))
            print("Found event links")
        except:
            print("Could not find event links, continuing anyway...")
        
        # Wait additional time for all content to render
        time.sleep(8)
        
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
    
    # Try to find JSON-LD structured data first (most reliable)
    events = []
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            import json
            data = json.loads(script.string)
            # Check if it's a list of events
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('@type') == 'Event':
                        events.append(item)
        except:
            continue
    
    if events:
        print(f"Found {len(events)} events from JSON-LD data")
        for event in events:
            try:
                # if contains "event series", then skip
                if "event series" in event.get('name', '').lower():
                    continue
                
                title = event.get('name', 'Title not found')
                event_url = event.get('url', '')
                
                # Skip if no valid title found
                if title == "Title not found":
                    continue
                
                # Filter out events with titles containing any of the filter substrings
                if any(keyword.lower() in title.lower() for keyword in title_filter_words):
                    continue
                
                # Get event time
                start_date = event.get('startDate', '')
                if start_date:
                    try:
                        # Parse ISO format datetime
                        event_start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                        # Convert to local time (HKT is UTC+8)
                        from datetime import timezone, timedelta
                        hkt = timezone(timedelta(hours=8))
                        event_start = event_start.astimezone(hkt)
                        
                        # Format time for display
                        event_time = event_start.strftime("%a, %b %d · %I:%M %p HKT")
                        
                        # Check if event is after work hours or on weekend
                        if not CommonUtils.is_time_after_work(event_start):
                            continue
                    except Exception as e:
                        print(f"Time parsing error for '{start_date}': {e}")
                        event_time = start_date
                else:
                    event_time = "Time not found"
                
                print(f"Time: {event_time}")
                print(f"Title: {title}")
                if event_url:
                    print(f"URL: {event_url}")
                print("-" * 40)
            except Exception as e:
                print(f"Error processing event: {e}")
                continue
        return
    
    # Fallback: Try HTML parsing with multiple strategies
    print("No JSON-LD data found, trying HTML parsing...")
    event_divs = []
    
    # Strategy 1: Try to find the event list container
    event_list_div = soup.find('div', class_="max-w-narrow")
    if event_list_div and hasattr(event_list_div, 'find_all'):
        event_divs = event_list_div.find_all('div', class_="w-full overflow-hidden")
        print(f"Found {len(event_divs)} events using strategy 1")
    
    # Strategy 2: Look for event cards directly if strategy 1 fails
    if not event_divs:
        # Try to find all links with time elements (typical event structure)
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            if link.find('time') and link.find('h2'):
                parent_div = link.parent
                if parent_div and parent_div.name == 'div':
                    event_divs.append(parent_div)
        print(f"Found {len(event_divs)} events using strategy 2")
    
    # Strategy 3: If still no events found, look for any time elements
    if not event_divs:
        time_elements = soup.find_all('time')
        for time_elem in time_elements:
            # Find the parent container
            parent = time_elem.find_parent('a')
            if parent and parent.find('h2'):
                event_divs.append(parent.parent if parent.parent else parent)
        print(f"Found {len(event_divs)} events using strategy 3")
    
    if not event_divs:
        print("Could not find any events on the page")
        # Save HTML for debugging
        with open('meetup_debug.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print("Saved page source to meetup_debug.html for debugging")
        return
    
    for event_div in event_divs:
        try:
            # if contains "event series", then skip
            if "event series" in event_div.text.lower():
                continue
            
            # Get the 'a' tag inside the event div
            a_tag = event_div if event_div.name == 'a' else event_div.find('a')
            if not a_tag:
                continue
            
            # Get the time
            time_element = a_tag.find('time')
            event_time = time_element.text.strip() if time_element else "Time not found"
            
            # Get the title
            title_element = a_tag.find('h2')
            if not title_element:
                # Try h3 or other heading tags
                title_element = a_tag.find(['h2', 'h3', 'h4'])
            title = title_element.text.strip() if title_element else "Title not found"
            
            # Skip if no valid title found
            if title == "Title not found":
                continue
            
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
            if event_url and not event_url.startswith('http'):
                event_url = f"https://www.meetup.com{event_url}"
            
            print(f"Time: {event_time}")
            print(f"Title: {title}")
            if event_url:
                print(f"URL: {event_url}")
            print("-" * 40)
        except Exception as e:
            print(f"Error processing event: {e}")
            continue
        
if __name__ == "__main__":
    from main import title_filter_config
    fetch_events(title_filter_config["meetup"])
