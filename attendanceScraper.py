import os
import time
import subprocess
import csv
from parse_data import parseData
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def load_credentials():
    load_dotenv()
    return os.getenv("USERNAME"), os.getenv("PASSWORD")

def send_notification(message):
    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "Attendance Update"'])

def parse_attendance():
    attendance_dict = {}
    with open("/Users/daksh-xyz/Desktop/Attendance/attendance_data.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        subject = ["ONM", "SE", "ISS", "DSML", "SEL", "ISSL", "IPPA", "MINOR", "OE"]
        i = 0
        for row in reader:
            if len(row) >= 10:
                subjecta = subject[i]
                attendance_percentage = row[10]
                attendance_dict[subjecta] = attendance_percentage
                i += 1
    
    message = "\n".join([f"{subject}: {percent}%" for subject, percent in attendance_dict.items()])
    send_notification(message)

def login_and_scrape():
    username, password = load_credentials()
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://mujslcm.jaipur.manipal.edu/")  # Replace with actual URL
    
    # Find username & password fields and submit
    driver.find_element(By.ID, "txtUserName").send_keys(username)
    driver.find_element(By.ID, "txtPassword").send_keys(password)
    driver.find_element(By.ID, "login_submitStudent").click()
    
    time.sleep(5)  # Wait for login
    driver.get("https://mujslcm.jaipur.manipal.edu/Student/Academic/AttendanceSummaryForStudent")  # Navigate to subpage
    
    time.sleep(2)  # Wait for content to load
    data = driver.find_element(By.ID, "dvDetail").text  # Adjust selector
    
    data_parser = parseData
    data_parser.parse_attendance_data(data)

    parse_attendance()
    
    driver.quit()
    print("Data saved to scraped_data.csv.")

if __name__ == "__main__":
    login_and_scrape()
