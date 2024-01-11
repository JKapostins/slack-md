from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

# Initialize WebDriver with options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Navigate to the website (required before setting cookies)
# Now the browser should be authenticated, and you can proceed with your automation script
driver.get('https://app.slack.com/client/T0ELQUJE4/C01RSNX4WQ3')

# Scroll up for 30 seconds
end_time = time.time() + 30
while time.time() < end_time:
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
    time.sleep(0.5)  # Adjust the sleep time as needed for smoother scrolling

# Load and add cookies
with open('path/to/cookies.json', 'r') as cookiesfile:
    cookies = json.load(cookiesfile)
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])  # Convert expiry time to int
        driver.add_cookie(cookie)

# Now you can navigate the browser as if it's a regular session
# Now the browser should be authenticated, and you can proceed with your automation script
driver.get('https://app.slack.com/client/T0ELQUJE4/C01RSNX4WQ3')

# Scroll up for 30 seconds
end_time = time.time() + 30
while time.time() < end_time:
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_UP)
    time.sleep(0.5)  # Adjust the sleep time as needed for smoother scrolling

# Now the browser should be authenticated, and you can proceed with your automation script
