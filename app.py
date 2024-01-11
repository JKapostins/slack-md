from selenium import webdriver
import json

# Initialize WebDriver with options
driver = webdriver.Chrome('/chrome-win64/chrome.exe')

# Navigate to the website (required before setting cookies)
driver.get('https://app.slack.com/client/T0ELQUJE4/C01RSNX4WQ3')

# Load and add cookies
with open('path/to/cookies.json', 'r') as cookiesfile:
    cookies = json.load(cookiesfile)
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])  # Convert expiry time to int
        driver.add_cookie(cookie)

# Now you can navigate the browser as if it's a regular session
driver.get('https://app.slack.com/client/T0ELQUJE4/C01RSNX4WQ3')

# Now the browser should be authenticated, and you can proceed with your automation script
