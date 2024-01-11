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
time.sleep(5)
# Proceed with automation tasks...
# Scroll up for 30 seconds
# Scroll up for 30 seconds and save content to a text file
content_selector = 'body > div.p-client_container > div > div > div.p-client_workspace_wrapper > div.p-client_workspace > div.p-client_workspace__layout > div:nth-child(2) > div:nth-child(2) > div > div > div.p-file_drag_drop__container > div.p-workspace__primary_view_body > div > div:nth-child(3) > div > div > div.c-scrollbar__hider'
end_time = time.time() + 30
with open('page_content.md', 'a', encoding='utf-8') as file:
    while time.time() < end_time:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
        time.sleep(0.5)
        with open('page_content.html', 'a', encoding='utf-8') as html_file:
            content_element_html = driver.find_element(By.CSS_SELECTOR, content_selector).get_attribute('outerHTML')
            html_file.write(content_element_html + "\n\n---\n\n")
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


        #TODO: content_element_html looks like HTML and i want it to be formeted like MARKDOWN. Please come up with a parser to do that. The parser should be generic as these elements appear multiple times for each message in in the html.
        #MARKDOWN:
        # ### ![](https://ca.slack-edge.com/T0ELQUJE4-U04137R0R1U-23dc45b70a8e-48) Pietro Belluno  [10:34 PM](https://fullstacklabs.slack.com/archives/C01RSNX4WQ3/p1704944089846389)  
        # `[NEW RELEASE][v1.7.3]` - v1.7.3 is live on `PRODUCTION` [@Ali Mazid](https://fullstacklabs.slack.com/team/U02HWTD22MT) [@Jaime Bustos](https://fullstacklabs.slack.com/team/U03QQPVFWP8) [@Jacob Kapostins](https://fullstacklabs.slack.com/team/U01TB5HFGNP) [@Todd Senkel](https://fullstacklabs.slack.com/team/U03G5PXLVND)\
        # ![:raised_hands:](https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-small/1f64c.png)2\
        # ![](https://ca.slack-edge.com/T0ELQUJE4-U02LLGP7ND9-gbc1683cad68-24)![](https://ca.slack-edge.com/T0ELQUJE4-U03G5PXLVND-fcc797f55797-24)![](https://ca.slack-edge.com/T0ELQUJE4-U04137R0R1U-23dc45b70a8e-24) [3 replies]() Last reply today at 8:27 AM

                #HTML:
        # <div aria-setsize="-1" class="c-virtual_list__item" tabindex="-1" role="listitem" id="1704944089.846389"
        #         data-qa="virtual-list-item" data-item-key="1704944089.846389" style="top: 2369px;">
        #         <div role="presentation"
        #             class="c-message_kit__background p-message_pane_message__message c-message_kit__message"
        #             data-qa="message_container" data-qa-unprocessed="false" data-qa-placeholder="false">
        #             <div role="document" aria-roledescription="message" class="c-message_kit__hover"
        #                 data-qa-hover="true">
        #                 <div class="c-message_kit__actions c-message_kit__actions--default" style="position: relative;">
        #                     <div class="c-message_kit__gutter">
        #                         <div role="presentation" class="c-message_kit__gutter__left"
        #                             data-stringify-ignore="true"><span class="p-member_profile_hover_card"
        #                                 role="presentation"><button
        #                                     class="c-button-unstyled c-message_kit__avatar c-avatar c-avatar--interactive"
        #                                     aria-hidden="true" aria-label="View Pietro Belluno’s Profile" tabindex="-1"
        #                                     type="button" style="height: 36px; width: 36px;"><span
        #                                         class="c-base_icon__width_only_container"
        #                                         style="height: 36px; width: 36px;"><img
        #                                             src="https://ca.slack-edge.com/T0ELQUJE4-U04137R0R1U-23dc45b70a8e-48"
        #                                             srcset="https://ca.slack-edge.com/T0ELQUJE4-U04137R0R1U-23dc45b70a8e-72 2x"
        #                                             class="c-base_icon c-base_icon--image" aria-hidden="true" role="img"
        #                                             alt="" style="width: 36px;"></span><span
        #                                         class="c-avatar__badge c-avatar__badge--ultra_restricted"><span
        #                                             class="c-avatar__badge_inner" delay="150"
        #                                             data-sk="tooltip_parent"></span></span></button></span></div>
        #                         <div role="presentation" class="c-message_kit__gutter__right" data-qa="message_content">
        #                             <span class="c-message__sender c-message_kit__sender" data-qa="message_sender"
        #                                 data-stringify-type="replace" data-stringify-text="Pietro Belluno"><span
        #                                     class="p-member_profile_hover_card" role="presentation"><button
        #                                         data-message-sender="U04137R0R1U" data-qa="message_sender_name"
        #                                         class="c-link--button c-message__sender_button" type="button">Pietro
        #                                         Belluno</button></span></span>&nbsp;&nbsp;<a
        #                                 aria-label="Yesterday at 10:34:49 PM" data-stringify-type="replace"
        #                                 data-stringify-text="[10:34 PM]" data-stringify-requires-siblings="true"
        #                                 data-ts="1704944089.846389" delay="300" data-sk="tooltip_parent"
        #                                 class="c-link c-timestamp"
        #                                 href="https://fullstacklabs.slack.com/archives/C01RSNX4WQ3/p1704944089846389"><span
        #                                     class="c-timestamp__label" data-qa="timestamp_label">10:34 PM</span></a><br>
        #                             <div class="c-message_kit__blocks c-message_kit__blocks--rich_text">
        #                                 <div class="c-message__message_blocks c-message__message_blocks--rich_text"
        #                                     data-qa="message-text">
        #                                     <div class="p-block_kit_renderer" data-qa="block-kit-renderer">
        #                                         <div
        #                                             class="p-block_kit_renderer__block_wrapper p-block_kit_renderer__block_wrapper--first">
        #                                             <div class="p-rich_text_block" dir="auto">
        #                                                 <div class="p-rich_text_section"><code
        #                                                         data-stringify-type="code"
        #                                                         class="c-mrkdwn__code">[NEW RELEASE][v1.7.3]</code> -
        #                                                     v1.7.3 is live on <code data-stringify-type="code"
        #                                                         class="c-mrkdwn__code">PRODUCTION</code> <span
        #                                                         class="p-member_profile_hover_card"
        #                                                         role="presentation"><a target="_blank"
        #                                                             class="c-link c-member_slug c-member_slug--light c-member_slug--link"
        #                                                             data-member-id="U02HWTD22MT"
        #                                                             data-member-label="@Ali Mazid"
        #                                                             data-stringify-type="mention"
        #                                                             data-stringify-id="U02HWTD22MT"
        #                                                             data-stringify-label="@Ali Mazid" tabindex="0"
        #                                                             aria-hidden="false"
        #                                                             href="https://fullstacklabs.slack.com/team/U02HWTD22MT"
        #                                                             rel="noopener noreferrer">@Ali Mazid</a></span>
        #                                                     <span class="p-member_profile_hover_card"
        #                                                         role="presentation"><a target="_blank"
        #                                                             class="c-link c-member_slug c-member_slug--light c-member_slug--link"
        #                                                             data-member-id="U03QQPVFWP8"
        #                                                             data-member-label="@Jaime Bustos"
        #                                                             data-stringify-type="mention"
        #                                                             data-stringify-id="U03QQPVFWP8"
        #                                                             data-stringify-label="@Jaime Bustos" tabindex="0"
        #                                                             aria-hidden="false"
        #                                                             href="https://fullstacklabs.slack.com/team/U03QQPVFWP8"
        #                                                             rel="noopener noreferrer">@Jaime Bustos</a></span>
        #                                                     <span class="p-member_profile_hover_card"
        #                                                         role="presentation"><a target="_blank"
        #                                                             class="c-link c-member_slug c-member_slug--light c-member_slug--link c-member_slug--mention"
        #                                                             data-member-id="U01TB5HFGNP"
        #                                                             data-member-label="@Jacob Kapostins"
        #                                                             data-stringify-type="mention"
        #                                                             data-stringify-id="U01TB5HFGNP"
        #                                                             data-stringify-label="@Jacob Kapostins" tabindex="0"
        #                                                             aria-hidden="false"
        #                                                             href="https://fullstacklabs.slack.com/team/U01TB5HFGNP"
        #                                                             rel="noopener noreferrer">@Jacob
        #                                                             Kapostins</a></span> <span
        #                                                         class="p-member_profile_hover_card"
        #                                                         role="presentation"><a target="_blank"
        #                                                             class="c-link c-member_slug c-member_slug--light c-member_slug--link"
        #                                                             data-member-id="U03G5PXLVND"
        #                                                             data-member-label="@Todd Senkel"
        #                                                             data-stringify-type="mention"
        #                                                             data-stringify-id="U03G5PXLVND"
        #                                                             data-stringify-label="@Todd Senkel" tabindex="0"
        #                                                             aria-hidden="false"
        #                                                             href="https://fullstacklabs.slack.com/team/U03G5PXLVND"
        #                                                             rel="noopener noreferrer">@Todd Senkel</a></span>
        #                                                 </div>
        #                                             </div>
        #                                         </div>
        #                                     </div>
        #                                 </div>
        #                             </div>
        #                             <div class="c-message_kit__reaction_bar c-reaction_bar c-reaction_bar--dark c-reaction_bar--collapsed"
        #                                 role="group" data-qa="reaction_bar" aria-label="Reactions"
        #                                 data-stringify-ignore="true"><button
        #                                     class="c-button-unstyled c-reaction c-reaction--dark"
        #                                     aria-label="2 reactions, react with raised hands emoji" aria-pressed="false"
        #                                     data-qa="reactji" delay="300" data-sk="tooltip_parent" type="button"><img
        #                                         src="https://a.slack-edge.com/production-standard-emoji-assets/14.0/google-small/1f64c.png"
        #                                         aria-label="raised hands emoji" alt=":raised_hands:"
        #                                         class="c-emoji c-emoji__small" data-qa="emoji"
        #                                         data-stringify-type="emoji" data-stringify-emoji=":raised_hands:"><span
        #                                         class="c-reaction__count">2</span></button><button
        #                                     class="c-button-unstyled c-reaction_add c-reaction_add--dark"
        #                                     aria-label="Add reaction..." data-qa="add_reaction_button" delay="300"
        #                                     data-sk="tooltip_parent" type="button">
        #                                     <div class="c-reaction_add__container"><i
        #                                             class="c-icon c-reaction_add__icon c-reaction_add__icon--bg c-icon--small-reaction-bg"
        #                                             type="small-reaction-bg" aria-hidden="true"></i><i
        #                                             class="c-icon c-reaction_add__icon c-reaction_add__icon--fg c-icon--small-reaction"
        #                                             type="small-reaction" aria-hidden="true"></i></div>
        #                                 </button></div>
        #                             <div role="presentation"
        #                                 class="c-message__reply_bar c-message_kit__thread_replies c-message__reply_bar--progressive-disclosure-tip-wrapper-ia4"
        #                                 data-qa="reply_bar" data-stringify-ignore="true"><span
        #                                     class="c-message__reply_bar_avatar c-avatar"
        #                                     style="height: 24px; width: 24px; --avatar-image-size: 24px;"><span
        #                                         class="c-base_icon__width_only_container"
        #                                         style="height: 24px; width: 24px;"><img
        #                                             src="https://ca.slack-edge.com/T0ELQUJE4-U02LLGP7ND9-gbc1683cad68-24"
        #                                             srcset="https://ca.slack-edge.com/T0ELQUJE4-U02LLGP7ND9-gbc1683cad68-48 2x"
        #                                             class="c-base_icon c-base_icon--image" aria-hidden="true" role="img"
        #                                             alt="" style="width: 24px;"></span></span><span
        #                                     class="c-message__reply_bar_avatar c-avatar"
        #                                     style="height: 24px; width: 24px; --avatar-image-size: 24px;"><span
        #                                         class="c-base_icon__width_only_container"
        #                                         style="height: 24px; width: 24px;"><img
        #                                             src="https://ca.slack-edge.com/T0ELQUJE4-U03G5PXLVND-fcc797f55797-24"
        #                                             srcset="https://ca.slack-edge.com/T0ELQUJE4-U03G5PXLVND-fcc797f55797-48 2x"
        #                                             class="c-base_icon c-base_icon--image" aria-hidden="true" role="img"
        #                                             alt="" style="width: 24px;"></span></span><span
        #                                     class="c-message__reply_bar_avatar c-avatar"
        #                                     style="height: 24px; width: 24px; --avatar-image-size: 24px;"><span
        #                                         class="c-base_icon__width_only_container"
        #                                         style="height: 24px; width: 24px;"><img
        #                                             src="https://ca.slack-edge.com/T0ELQUJE4-U04137R0R1U-23dc45b70a8e-24"
        #                                             srcset="https://ca.slack-edge.com/T0ELQUJE4-U04137R0R1U-23dc45b70a8e-48 2x"
        #                                             class="c-base_icon c-base_icon--image" aria-hidden="true" role="img"
        #                                             alt="" style="width: 24px;"></span></span><button
        #                                     data-qa="reply_bar_count" aria-expanded="false"
        #                                     class="c-link--button c-message__reply_count" type="button">3
        #                                     replies</button>
        #                                 <div class="c-message__reply_bar_description"><span
        #                                         class="c-message__reply_bar_last_reply"
        #                                         data-qa="reply_bar_last_reply">Last reply today at 8:27 AM</span><span
        #                                         class="c-message__reply_bar_view_thread"
        #                                         data-qa="reply_bar_view_thread">View thread</span></div><i
        #                                     class="c-deprecated-icon c-message__reply_bar_arrow c-icon--chevron-right c-deprecated-icon--vertical-align-baseline"
        #                                     type="chevron_right" aria-hidden="true"></i>
        #                             </div>
        #                         </div>
        #                     </div>
        #                 </div>
        #             </div>
        #         </div>
        #     </div>
        soup = BeautifulSoup(content_element_html, 'html.parser')
        markdown_content = ''
        for element in soup.find_all(True, recursive=False):
            if 'c-virtual_list__item' in element.get('class', []):
                markdown_content += '\n\n'  # Add extra newline before each c-virtual_list__item
            element_html = str(element)
            element_markdown = md(element_html)
            markdown_content += element_markdown
        markdown_content += '\n\n'
        file.write(markdown_content + "\n\n---\n\n")
        break
