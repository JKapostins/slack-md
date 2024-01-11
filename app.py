from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from selenium.webdriver.common.keys import Keys

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
# Scroll up for 30 seconds
end_time = time.time() + 30
while time.time() < end_time:
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
    time.sleep(0.5) 