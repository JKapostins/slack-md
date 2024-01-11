from selenium import webdriver
from selenium.webdriver.common.by import By
from markdownify import markdownify as md
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
# Proceed with automation tasks...
# Scroll up for 30 seconds
# Scroll up for 30 seconds and save content to a text file
content_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(2) > div:nth-child(2) > div > div > div.p-file_drag_drop__container > div.p-workspace__primary_view_body > div > div:nth-child(3) > div > div > div.c-scrollbar__hider'
end_time = time.time() + 30
with open('page_content.md', 'a', encoding='utf-8') as file:
    while time.time() < end_time:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
        time.sleep(0.5)
        # Find and click buttons with the specified selector
        # buttons = driver.find_elements(By.CSS_SELECTOR, 'button')
        # for button in buttons:
        #     try:
        #         #\31 704944089\.846389 > div > div > div > div > div.c-message_kit__gutter__right > div.c-message__reply_bar.c-message_kit__thread_replies.c-message__reply_bar--progressive-disclosure-tip-wrapper-ia4 > button
        #         if 'c-message__reply_count' in button.get_attribute('class'):
        #             driver.execute_script("arguments[0].click();", button)
        #     except Exception as e:
        #         print(f"Error clicking button: {e}")
        content_element_html = driver.find_element(By.CSS_SELECTOR, content_selector).get_attribute('outerHTML')
        markdown_content = md(content_element_html)
        file.write(markdown_content + "\n\n---\n\n")