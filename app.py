from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import json
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import uuid  # Import uuid module
import requests
import os

thread_folder = 'threads'
if not os.path.exists(thread_folder):
    os.makedirs(thread_folder)

processed_threads = set()

# Initialize WebDriver with options
options = webdriver.ChromeOptions()

# Specify the desired download folder
#download_folder = "C:/path/to/download/folder"
#set download folder to working directory
download_folder = os.getcwd() + "\downloads"
prefs = {"download.default_directory": download_folder}
options.add_experimental_option("prefs", prefs)
#options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
# Dictionary to maintain sets of processed dividers for each thread and the main file
processed_dividers_dict = {'main': set()}
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


def download_file_with_cookies(file_url, save_path, driver):
    with requests.Session() as s:
        for cookie in driver.get_cookies():
            s.cookies.set(cookie['name'], cookie['value'])

        response = s.get(file_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

def convert_html_to_markdown(html_content, thread_links, image_download_folder='downloads', driver=None, thread_id='main'):
    # Use the set corresponding to the thread_id or the main file
    processed_dividers = processed_dividers_dict.setdefault(thread_id, set())
    
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_contents = []  # List to hold all markdown content

    if not os.path.exists(image_download_folder):
        os.makedirs(image_download_folder)

    for item in soup.select('.c-virtual_list__item, .c-message_list__day_divider__label'):
        # Skip item if it's already been processed
        if item.get('data-processed', '') == 'true':
            continue
        
    # Check if it's a day divider
        day_label = item.select_one('.c-message_list__day_divider__label__pill')
        if day_label:
            day_text = day_label.get_text(strip=True)
            if day_text not in processed_dividers:
                markdown_contents.append(f"# {day_text}\n\n")
                processed_dividers.add(day_text)
        
        else:
            user_name_element = item.select_one('.c-message__sender')
            if not user_name_element:
                continue  # Skip to next element if user name is null

            timestamp_element = item.select_one('.c-timestamp__label')
            message_text_element = item.select_one('.c-message__message_blocks')
            reply_bar_element = item.select_one('.c-message__reply_bar')

            user_name = user_name_element.get_text(strip=True)
            timestamp = timestamp_element.get_text(strip=True) if timestamp_element else "Unknown Time"

            message_text = ''
            if message_text_element:
                # Convert <pre> elements for multi-line code blocks
                for pre in message_text_element.find_all('pre'):
                    code_text = pre.get_text()
                    pre.replace_with(f"```{code_text}```")

                # Convert <code> elements for single-line code blocks
                for code in message_text_element.find_all('code'):
                    code.replace_with(f" `{code.get_text(strip=True)}` ")

                # Convert <a> elements (hyperlinks) and add spaces
                for a_tag in message_text_element.find_all('a'):
                    href = a_tag.get('href', '')
                    link_text = a_tag.get_text(strip=True)
                    a_tag.replace_with(f" [{link_text}]({href}) ")

                message_text = message_text_element.get_text(strip=True)

                # General text formatting for spacing
                message_text = re.sub(r'`(\s)?([^`]+)(\s)?`', r' `\2` ', message_text)  # Ensure space around code blocks
                message_text = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r' [\1](\2) ', message_text)  # Ensure space around links
                message_text = message_text.replace("` ``", "\n\n```\n\n")  # Fix multi line code blocks
                message_text = message_text.replace("`` `", "\n\n```\n\n")  # Fix multi line code blocks


            reply_bar_text = ''
            if reply_bar_element:
                avatars = reply_bar_element.find_all('img', class_='c-base_icon')
                reply_count = reply_bar_element.select_one('.c-message__reply_count')
                last_reply = reply_bar_element.select_one('.c-message__reply_bar_last_reply')

                avatar_images = ' '.join(f"![]({avatar['src']})" for avatar in avatars if avatar.get('src'))
                reply_count_text = reply_count.get_text(strip=True) if reply_count else ""
                last_reply_text = last_reply.get_text(strip=True) if last_reply else ""

                thread_markdown_link = ''
                button = item.find('button', {'class': 'c-message__reply_count'})
                if button and 'data-thread-id' in button.attrs:
                    thread_id = button['data-thread-id']
                    thread_markdown_link = thread_links.get(thread_id, '')
                reply_bar_text = f"{avatar_images} [{reply_count_text}](/{thread_markdown_link}) {last_reply_text}"

            
            #Find and process video messages
            video_element = item.select_one('.p-video_message_file')
            video_markdown = ''
            if video_element and video_element.get('data-processed') != 'true':
                video_label = video_element.find('div', {'class': 'p-video_controls_overlay'}).get('aria-label')
                if video_label:
                    # Process the video as before...
                    video_path = f"{image_download_folder}/{video_label}"

                    # Find the 'More Actions' button for the video
                    more_actions_button = driver.find_element(By.CSS_SELECTOR, '.p-video_message_file__controls_overlay_ellipsis')
                    driver.execute_script("arguments[0].click();", more_actions_button)

                    # Wait for the 'Download' button to appear and click it
                    download_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(div, 'Download')]"))
                    )
                    download_button.click()

                    # Assuming the video will be automatically downloaded by the browser
                    # Wait or check for the download to complete here, if necessary
                    video_path = video_path.replace(" ", "%20")
                    video_markdown += f"[Download Video](/{video_path})\n\n"

                    # Mark the video element as processed
                    video_element['data-processed'] = 'true'

            file_elements = item.select('.c-files_container')
            file_markdown = ''
            for file_element in file_elements:
                file_link_tag = file_element.select_one('a.c-link')
                if file_link_tag:
                    file_url = file_link_tag.get('href')
                    # Generate a unique filename using UUID
                    file_extension = os.path.splitext(file_url)[1]
                    file_name_with_extension = f"{str(uuid.uuid4())}{file_extension}"
                    file_path = os.path.join(image_download_folder, file_name_with_extension)

                    if '?' in file_path:
                        file_path = file_path.split('?')[0]

                    download_file_with_cookies(file_url, file_path, driver)
                    #check if file extension is an image
                    if file_extension in ['.png', '.jpg', '.jpeg', '.gif']:
                        file_markdown += f"![]({file_path})\n\n"
                    else:
                        file_name_element = file_element.select_one('span[data-qa="file-meta-text"]')
                        file_name = 'File'
                        if file_name_element:
                            file_name = file_name_element.get_text(strip=True)
                        file_markdown += f"[Download {file_name}]({file_path})\n\n"


            markdown_content = f"### {user_name}  [{timestamp}]\n\n{message_text}\n\n{video_markdown}{file_markdown}{reply_bar_text}\n\n---\n\n"
            markdown_contents.append(markdown_content)

        # Mark item as processed in the browser
        item_id = item.get('id')
        if item_id:
            try:
                web_element = driver.find_element(By.ID, item_id)
                # Mark as processed in the browser
                driver.execute_script("arguments[0].setAttribute('data-processed', 'true')", web_element)
            except Exception as e:
                print(f"Error marking element as processed: {e}")


    return ''.join(markdown_contents)


def handle_thread(button, driver, thread_links, image_download_folder, thread_folder):
    thread_id = button.get_attribute("data-thread-id")
    if not thread_id:
        thread_id = str(uuid.uuid4())
        driver.execute_script("arguments[0].setAttribute('data-thread-id', arguments[1])", button, thread_id)

    if thread_id in processed_threads:
        return

    # Get the number of replies from the button text
    number_of_replies = int(button.text.split()[0]) + 1 #add 1 to account for the original message  # Assuming the text format is like "70 replies"

    driver.execute_script("arguments[0].click();", button)
    time.sleep(1)

    thread_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(3) > div:nth-child(2) > div'
    thread_element = driver.find_element(By.CSS_SELECTOR, thread_selector)
    input_selector = '.c-texty_input_unstyled'
    thread_md_contents = []

    reverse = False
    # Initialize variables to track count changes and time
    last_count_change_time = time.time()
    previous_count = 0
    while True:
        thread_element = driver.find_element(By.CSS_SELECTOR, thread_selector)
        thread_html = thread_element.get_attribute('outerHTML')
        md_content = convert_html_to_markdown(thread_html, {}, image_download_folder, driver, thread_id)

        #count the number of times "# " appears in the md_content
        # if md_content.count("### ") >= number_of_replies:
        #     break

        if md_content:
            thread_md_contents.append(md_content)
        
        count = sum(s.count("### ") for s in thread_md_contents)  
        if(count >= number_of_replies):
            break

        # Check if count has changed
        if count != previous_count:
            previous_count = count
            last_count_change_time = time.time()

        # Check if 10 seconds have passed without a count change
        if time.time() - last_count_change_time >= 10:
            # Perform PAGE UP and PAGE DOWN to unstuck
            if reverse:
                list_items = thread_element.find_elements(By.CSS_SELECTOR, '.c-virtual_list__item')
                if(list_items):
                    first_item = list_items[0]
                    first_item.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            else:
                list_items = thread_element.find_elements(By.CSS_SELECTOR, '.c-virtual_list__item')
                if(list_items):
                    last_item = list_items[-1]
                    last_item.send_keys(Keys.PAGE_UP)
            time.sleep(1)  # Short delay

        try:
            WebDriverWait(thread_element, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, input_selector)))

            if number_of_replies > 20:
                reverse = True
                # Scroll up if the number of replies is high and the input field is visible
                list_items = thread_element.find_elements(By.CSS_SELECTOR, '.c-virtual_list__item')

                if(list_items):
                    first_item = list_items[0]
                    first_item.send_keys(Keys.PAGE_UP)
                else:
                    break
            else:
                # If there are fewer replies and input field is visible, exit the loop
                break
        except TimeoutException:
            # Scroll down if the input field is not visible
            list_items = thread_element.find_elements(By.CSS_SELECTOR, '.c-virtual_list__item')
            if(list_items):
                last_item = list_items[-1]
                last_item.send_keys(Keys.PAGE_DOWN)
            else:
                break

        time.sleep(1)

        
    if reverse:
        thread_md_contents.reverse()

    thread_md_filename = os.path.join(thread_folder, f'thread_{thread_id}.md')
    with open(thread_md_filename, 'w', encoding='utf-8') as md_file:
        for content in thread_md_contents:
            md_file.write(content)

    thread_links[thread_id] = thread_md_filename
    driver.execute_script("arguments[0].setAttribute('data-processed', 'true')", button)
    processed_threads.add(thread_id)

    close_thread_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(3) > div:nth-child(2) > div > div > div > div.p-flexpane_header > div > button'
    close_thread_button = driver.find_element(By.CSS_SELECTOR, close_thread_selector)
    driver.execute_script("arguments[0].click();", close_thread_button)




# def handle_thread(button, driver, thread_links, image_download_folder, thread_folder):
#     # Assign a unique ID to the thread if it doesn't have one
#     thread_id = button.get_attribute("data-thread-id")
#     if not thread_id:
#         thread_id = str(uuid.uuid4())
#         driver.execute_script("arguments[0].setAttribute('data-thread-id', arguments[1])", button, thread_id)

#     # Check if the thread has already been processed
#     if thread_id in processed_threads:
#         return

#     driver.execute_script("arguments[0].click();", button)
#     time.sleep(1)  # Wait for the thread to load

#     # Selector for the thread content
#     thread_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(3) > div:nth-child(2) > div'
#     input_selector = '.c-texty_input_unstyled'
#     # Initialize an empty list to store markdown content for the thread
#     thread_md_contents = []

#      # Determine whether to scroll up or down
#     need_to_scroll_up = False
#     while True:
#         thread_element = driver.find_element(By.CSS_SELECTOR, thread_selector)

#         try:
#             # Check for the visibility of the input element
#             WebDriverWait(thread_element, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, input_selector)))
#             if need_to_scroll_up:
#                 break  # If scrolling up and input is visible, exit the loop
#         except TimeoutException:
#             pass  # Input not visible yet

#         # Capture content
#         thread_html = thread_element.get_attribute('outerHTML')
#         md_content = convert_html_to_markdown(thread_html, {}, image_download_folder, driver, thread_id)

#         # Add content to the list
#         if md_content:
#             thread_md_contents.append(md_content)

#         # Determine scroll direction
#         if not need_to_scroll_up:
#             list_items = thread_element.find_elements(By.CSS_SELECTOR, '.c-virtual_list__item')
#             if list_items:
#                 first_item = list_items[0]
#                 first_item_id_before_scroll = first_item.get_attribute('id')

#                 # Scroll and check if the first item changes
#                 first_item.send_keys(Keys.PAGE_DOWN)
#                 time.sleep(0.5)
#                 first_item_id_after_scroll = first_item.get_attribute('id')

#                 if first_item_id_before_scroll == first_item_id_after_scroll:
#                     need_to_scroll_up = True
#             else:
#                 break  # No items to scroll

#         if need_to_scroll_up:
#             # If we need to scroll up, use PAGE_UP
#             driver.execute_script("arguments[0].scrollTop -= 1000;", thread_element)
#             time.sleep(0.5)

#         #--------------------------------
#         # thread_element = driver.find_element(By.CSS_SELECTOR, thread_selector)

#         # thread_html = driver.find_element(By.CSS_SELECTOR, thread_selector).get_attribute('outerHTML')
#         # md_content = convert_html_to_markdown(thread_html, {}, image_download_folder, driver, thread_id)

#         # if md_content:
#         #     thread_md_contents.append(md_content)

#         # try:
#         #     # Wait for the input element to be visible within the thread element
#         #     WebDriverWait(thread_element, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, input_selector)))
#         #     break  # Input element is loaded, exit the loop
#         # except TimeoutException:
#         #     # Press PAGE_DOWN key to scroll down and continue waiting
#         #     list_items = thread_element.find_elements(By.CSS_SELECTOR, '.c-virtual_list__item')
#         #     if(list_items):
#         #         last_item = list_items[-1]
#         #         last_item.send_keys(Keys.PAGE_DOWN)
#         #     else:
#         #         break
#         #     #driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
#         #     time.sleep(1)

#     thread_md_contents.reverse()
#     thread_md_filename = os.path.join(thread_folder, f'thread_{thread_id}.md')
#     with open(thread_md_filename, 'w', encoding='utf-8') as md_file:
#         for content in thread_md_contents:
#             md_file.write(content)


#     thread_links[thread_id] = thread_md_filename

#     # Mark this thread as processed
#     driver.execute_script("arguments[0].setAttribute('data-processed', 'true')", button)
#     # Add the thread ID to the processed_threads set
#     processed_threads.add(thread_id)

#     # Close the thread after processing
#     close_thread_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(3) > div:nth-child(2) > div > div > div > div.p-flexpane_header > div > button'
#     close_thread_button = driver.find_element(By.CSS_SELECTOR, close_thread_selector)
#     driver.execute_script("arguments[0].click();", close_thread_button)



# Navigate to the specific Slack workspace URL
driver.get('https://app.slack.com/client/T0ELQUJE4/C01RSNX4WQ3')
time.sleep(5)
# Proceed with automation tasks...
# Scroll up for 30 seconds
# Scroll up for 30 seconds and save content to a text file


main_content_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(2) > div:nth-child(2) > div > div > div.p-file_drag_drop__container > div.p-workspace__primary_view_body > div > div:nth-child(3) > div > div > div.c-scrollbar__hider'

thread_links = {}
md_content_list = []
# Initialize the last scroll top position
last_scroll_top = -1

# Continue until there's no more new content to scroll to
while True:
    # Scroll up
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
    time.sleep(0.5)  # Adjust sleep time as needed

    # Get the current scroll position
    scroll_element = driver.find_element(By.CSS_SELECTOR, main_content_selector)

    # Find and click buttons to open thread replies
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button.c-message__reply_count')
    for button in buttons:
        handle_thread(button, driver, thread_links, 'downloads', thread_folder)

    # Get the HTML content and convert it to Markdown
    content_element_html = scroll_element.get_attribute('outerHTML')
    md_content = convert_html_to_markdown(content_element_html, thread_links, 'downloads', driver)

    # When the channel was started.
    if md_content.find("# March 18th, 2021") != -1:
        break

    # # break early for testing
    # if md_content.find("# December 1st, 2023") != -1:
    #     break
        
    # Append the new markdown content to the list
    md_content_list.append(md_content)

# Reverse the list to have the oldest content at the top
md_content_list.reverse()

# Write the reversed content to the Markdown file
with open('page_content.md', 'w', encoding='utf-8') as md_file:
    for content in md_content_list:
        md_file.write(content)

driver.quit()


