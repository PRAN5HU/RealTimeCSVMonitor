import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration with credentials and URL
config = {
    'EMAIL': os.getenv('EMAIL'),
    'PASSWORD': os.getenv('PASSWORD')
}

login_url = os.getenv('LOGIN_URL')
target_url = os.getenv('TARGET_URL')

def create_csv_file(csv_file_path):
    # Check if the CSV file exists
    file_exists = os.path.isfile(csv_file_path)

    # Create the CSV file if it doesn't exist
    if not file_exists:
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Data Value'])
        print("Successfully created a CSV file.")

def fetch_data(driver, csv_file_path):
    try:
        # Navigate to the target URL
        driver.get(target_url)

        # Wait for the page to load completely
        time.sleep(5)

        # Fetch the latest data value (Adjust the XPath to select the correct row and cell)
        latest_row = driver.find_element(By.XPATH, "(//tr)[2]")  # Adjust the XPath as needed to select the correct row
        latest_data_value = latest_row.find_elements(By.TAG_NAME, 'td')[2].text  # Adjust the index if needed

        print("Latest Data Value:", latest_data_value)

        # Write the data to the CSV file
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the current timestamp and data value
            writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), latest_data_value])
        print("Values updated to CSV file.")

    except Exception as e:
        print("Error fetching data:", e)

def main():
    # Specify the path to the chromedriver executable
    chromedriver_path = "C:/path/to/chromedriver"

    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Optional: maximize the browser window

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    try:
        # Navigate to the login URL
        driver.get(login_url)

        # Find the username field and enter the username
        username_field = driver.find_element(By.ID, 'username_field_id')  # Update ID as needed
        username_field.clear()
        username_field.send_keys(config['EMAIL'])

        # Find the password field and enter the password
        password_field = driver.find_element(By.ID, 'password_field_id')  # Update ID as needed
        password_field.clear()
        password_field.send_keys(config['PASSWORD'])

        # Find the sign-in button and click it
        sign_in_button = driver.find_element(By.XPATH, "//button[@type='submit']")  # Update XPath as needed
        sign_in_button.click()

        # Wait for some time to ensure the login process completes
        time.sleep(5)

        # Define the CSV file path
        csv_file_path = 'data_values.csv'

        # Create the CSV file if it doesn't exist
        create_csv_file(csv_file_path)

        # Enter an infinite loop to keep fetching and storing data
        while True:
            fetch_data(driver, csv_file_path)
            # Wait for 2 minutes before fetching data again
            time.sleep(120)

    except Exception as e:
        print("Error during login:", e)

    finally:
        # Close the driver
        driver.quit()

# Call the main function directly
if __name__ == "__main__":
    main()
