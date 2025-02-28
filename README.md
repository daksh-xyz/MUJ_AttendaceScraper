# MacOS Automated Web Scraper

This project is a macOS automation script that logs into MUJ slcm portal, scrapes attendance data, and sends a macOS notification with the attendance percentage.

## Features
- **Automated login**: Uses `requests` to log in to the website.
- **macOS Notifications**: Displays attendance data as a system notification.
- **Automated Execution**: Runs at a scheduled time using AppleScript and Automator.

## Installation

### 1. Install Dependencies
Ensure you have Python 3 and the required libraries:
```bash
pip install python-dotenv requests  bs4
```

### 2. Configure Credentials
Create a `.env` file in the same directory as the script and add:
```
USERNAME=your_username
PASSWORD=your_password
```
Replace `your_username` and `your_password` with your actual credentials.

### 3. Set Up Automator

#### Create an Automator App
1. Open **Automator** (`Cmd + Space` → Search "Automator").
2. Click **New Document** → Choose **Application**.
3. Add **Run AppleScript** action and paste:
   ```applescript
   do shell script "usr/local/bin/python3 /Users/your-username/path/to/attendanceScraper.py"
   ```
4. Save it as `WebScraperApp`.

#### Schedule in macOS Calendar
1. Open **Calendar**.
2. Create a new event at your desired time.
3. Click **Alert > Custom**.
4. Select **Open File** and choose **Other**.
5. Open **path/to/WebScraperApp** and choose **WebScraperApp**.
6. Set to open **At Time of Event**.

## Usage
- The script will run at the scheduled time, log in, scrape data and send a notification.
- To run manually, execute:
  ```bash
  python3 attendanceScraper.py
  ```

## Troubleshooting
- Open Script Editor once and type this command:
    ```bash
    display notification "Hello" with title "Test"
    ```
- run the script
- script editor will ask for permission to display notifications, click on allow!

## License
This project is for personal use only. Modify and distribute as needed!