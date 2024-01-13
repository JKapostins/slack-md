# Slack Channel Archiver

This project is designed to archive Slack channels into markdown files. It automates the process of converting Slack messages, including threads and file attachments, into a markdown format that can be easily saved and viewed outside of Slack.

## Installation

To run the Slack Channel Archiver, you need to install the required dependencies. These dependencies are listed in the `requirements.txt` file. To install them, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

Make sure you have Python and `pip` installed on your system before running the above command.

## ChromeDriver Installation

The Slack Channel Archiver uses Selenium, which requires ChromeDriver to interact with the Chrome browser. You must install ChromeDriver that matches the version of Chrome installed on your system. Follow these steps to install ChromeDriver:

1. Check the version of Chrome installed on your system by navigating to `chrome://version/` in your Chrome browser.
2. Visit the [ChromeDriver download page](https://sites.google.com/a/chromium.org/chromedriver/downloads).
3. Download the version of ChromeDriver that corresponds to your Chrome version.
4. Extract the downloaded file and place `chromedriver` in a known location on your system.
5. Add the location of `chromedriver` to your system's PATH environment variable so that it can be accessed from the command line.

After installing ChromeDriver, you can proceed with running the `app.py` script as described in the Usage section.

## Usage

After installing the dependencies, you can run the `app.py` script to start the archiving process. The script will navigate through the Slack workspace, download files, and convert the content into markdown format.

## Note

Before running the script, ensure you have the necessary authentication cookies from Slack stored in a `cookies.json` file, as the script uses these cookies to access the Slack workspace.

## Creating the Cookies File

To create the `cookies.json` file, you can use the EditThisCookie browser extension, which is available for Chrome and other browsers. Follow these steps:

1. Install the EditThisCookie extension from your browser's extension store.
2. Navigate to your Slack workspace in the browser and sign in.
3. Select the channel you wish to archive.
4. Copy the URL of the selected channel; you will use this as input into `app.py`.
5. After you are signed in, navigate to `https://slack.com` to ensure you are on the main Slack domain.
6. Click on the EditThisCookie extension icon in your browser toolbar.
7. In the EditThisCookie panel, click the export button to copy all cookies to your clipboard.
8. Paste the copied cookies into a new file and save it as `cookies.json` in the same directory as your `app.py` script.

**Warning:** You must export the cookies from `https://slack.com` and not your Slack workspace URL to avoid a domain mismatch error when loading the cookies in the script.

1. Install the EditThisCookie extension from your browser's extension store.
2. Log in to your Slack workspace in the browser.
3. Click on the EditThisCookie extension icon in your browser toolbar.
4. In the EditThisCookie panel, click the export button to copy all cookies to your clipboard.
5. Paste the copied cookies into a new file and save it as `cookies.json` in the same directory as your `app.py` script.

Make sure that the `cookies.json` file is correctly formatted as a JSON array of cookie objects before attempting to run the script.
