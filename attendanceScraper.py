import requests
from bs4 import BeautifulSoup
import subprocess
from dotenv import load_dotenv
import os
import socket

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Define URLs
LOGIN_URL = "https://mujslcm.jaipur.manipal.edu"
ATTENDANCE_URL = "https://mujslcm.jaipur.manipal.edu/Student/Academic/GetAttendanceSummaryList"

def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        return True
    except OSError:
        return False

# Check internet connection
if not is_connected():
    print("No internet connection! Please check your network.")
    subprocess.run(["osascript", "-e", 'display notification "No internet connection!" with title "Error"'])
    exit()

# Define headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Referer": LOGIN_URL,
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest"
}

# Create a session to maintain login state
session = requests.Session()

# Get the login page to fetch CSRF token
response = session.get(LOGIN_URL, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find("input", {"name": "__RequestVerificationToken"})
if csrf_token:
    csrf_token = csrf_token["value"]
else:
    print("CSRF token not found!")
    exit()

# Define user credentials (replace with actual credentials)
credentials = {
    "__RequestVerificationToken": csrf_token,
    "EmailFor": "@muj.manipal.edu",
    "LoginFor": "2",
    "UserName": USERNAME,  # Adjust based on the form field name
    "Password": PASSWORD,
}


# Log in to the website
response = session.post(LOGIN_URL, data=credentials, headers=headers)
if "login-panel" in response.text:
    print("Login failed! Check credentials.")
    exit()

credentials["StudentCode"] = ""

response = session.post(ATTENDANCE_URL, headers=headers, data=credentials)

# Parse JSON response
if response.status_code == 200:
    data = response.json()
    attendance_list = data.get("AttendanceSummaryList", [])
    message = ""
    courses = ["ONM", "SE", "ISS", "DSML", "SEL", "ISSL", "IPPA", "MP", "OE"]
    i = 0
    for entry in attendance_list:
        course = courses[i]
        percentage = entry['Percentage']
        message += f"{course}: {percentage}%\n"
        i += 1
        
        # Show macOS notification
    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "Attendance Update"'])

else:
    subprocess.run(["osascript", "-e", f'display notification "Invalid Credentials/No Internet" with title "Attendance Update"'])