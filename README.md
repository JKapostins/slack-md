# Slack Channel Archiver

This project is designed to archive Slack channels into markdown files. It automates the process of converting Slack messages, including threads and file attachments, into a markdown format that can be easily saved and viewed outside of Slack.

## Installation

To run the Slack Channel Archiver, you need to install the required dependencies. These dependencies are listed in the `requirements.txt` file. To install them, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

Make sure you have Python and `pip` installed on your system before running the above command.

## Usage

After installing the dependencies, you can run the `app.py` script to start the archiving process. The script will navigate through the Slack workspace, download files, and convert the content into markdown format.

## Note

Before running the script, ensure you have the necessary authentication cookies from Slack stored in a `cookies.json` file, as the script uses these cookies to access the Slack workspace.

## Creating the Cookies File

To create the `cookies.json` file, you can use the EditThisCookie browser extension, which is available for Chrome and other browsers. Follow these steps:

1. Install the EditThisCookie extension from your browser's extension store.
2. Log in to your Slack workspace in the browser.
3. Click on the EditThisCookie extension icon in your browser toolbar.
4. In the EditThisCookie panel, click the export button to copy all cookies to your clipboard.
5. Paste the copied cookies into a new file and save it as `cookies.json` in the same directory as your `app.py` script.

Make sure that the `cookies.json` file is correctly formatted as a JSON array of cookie objects before attempting to run the script.
