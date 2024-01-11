from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Initialize WebDriver with options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Navigate to a base domain of Slack
driver.get('https://slack.com/')
time.sleep(5)
# Load and add cookies
with open('cookies.json', 'r') as cookiesfile:
    cookies = json.load(cookiesfile)
    for cookie in cookies:
        # Format the cookie to be compatible with Selenium
        formatted_cookie = {k: v for k, v in cookie.items() if k in ['name', 'value', 'domain', 'path', 'expiry', 'secure']}
        if 'expiry' in formatted_cookie:
            formatted_cookie['expiry'] = int(formatted_cookie['expiry'])
        driver.add_cookie(formatted_cookie)

# Navigate to the specific Slack workspace URL
driver.get('https://app.slack.com/client/T0ELQUJE4/C01RSNX4WQ3')
time.sleep(5)
# Proceed with automation tasks...
# Scroll up for 30 seconds
# Scroll up for 30 seconds and save content to a text file
content_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(2) > div:nth-child(2) > div > div > div.p-file_drag_drop__container > div.p-workspace__primary_view_body > div > div:nth-child(3) > div > div > div.c-scrollbar__hider'
end_time = time.time() + 30
with open('page_content.txt', 'a') as file:
with open('page_content.txt', 'a', encoding='utf-8') as file:
    while time.time() < end_time:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
        time.sleep(0.5)
        content_element = driver.find_element(By.CSS_SELECTOR, content_selector)
        file.write(content_element.text + "\n\n---\n\n")
    time.sleep(0.5) 