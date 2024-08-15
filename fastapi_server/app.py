from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import json
import requests
import datetime

# Configure WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
service = Service(executable_path='/path/to/chromedriver')  # Update the path to chromedriver

# Initialize the WebDriver
driver = webdriver.Chrome()

# Set up WebDriver wait
wait = WebDriverWait(driver, 10)

try:
    for i in range(21, 41):
        try:
            driver.get("https://www.gturesults.in/")

            # To select particular stream, sem, and branch
            select_element = wait.until(EC.presence_of_element_located((By.ID, "ddlbatch")))
            select = Select(select_element)
            select.select_by_visible_text(".....BE SEM 6 - Regular (MAY 2024)")

            # For enrollment field
            enrollment_no_field = wait.until(EC.presence_of_element_located((By.ID, "txtenroll")))
            enrollment_no = f"2112401070{i}"
            enrollment_no_field.clear()  # Clear any pre-existing text
            enrollment_no_field.send_keys(enrollment_no)

            # Captcha code image
            img_element = wait.until(EC.presence_of_element_located((By.ID, "imgCaptcha")))
            img_screenshot = img_element.screenshot_as_png

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"captcha_{enrollment_no}_{timestamp}.jpg"
            file_path = os.path.join(os.getcwd(), filename)

            # Save the image to a file
            with open(file_path, 'wb') as f:
                f.write(img_screenshot)

            # Send the screenshot to the API
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f, 'image/jpeg')}
                url = "http://localhost:8000/extract-text"
                response = requests.post(url, files=files)
                response.raise_for_status()  # Raise an exception for HTTP errors
                response_data = response.json()
                captcha_code = response_data.get('extracted_text', '').strip('~~')

                # Input the captcha code and click the submit button
                captcha_input_field = wait.until(EC.presence_of_element_located((By.ID, "CodeNumberTextBox")))
                captcha_input_field.clear() 
                captcha_input_field.send_keys(captcha_code)

                submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnSearch")))
                submit_button.click()

                # Result data extraction
                try:
                    name_field = wait.until(EC.presence_of_element_located((By.ID, 'lblName')))
                    
                    if name_field.text == '------------':
                        continue
                    
                    spi_field = wait.until(EC.presence_of_element_located((By.ID, 'lblSPI')))
                    cpi_field = wait.until(EC.presence_of_element_located((By.ID, 'lblCPI')))
                    cgpa_field = wait.until(EC.presence_of_element_located((By.ID, 'lblCGPA')))
                    
                    print(f"Enrollment: {enrollment_no}")
                    print(f"Name: {name_field.text}")
                    print(f"SPI: {spi_field.text}")
                    print(f"CPI: {cpi_field.text}")
                    print(f"CGPA: {cgpa_field.text}")
                    
                except Exception as e:
                    print(f"Failed to extract result data for enrollment number {enrollment_no}: {e}")

        except Exception as e:
            print(f"An error occurred for enrollment number {enrollment_no}: {e}")

finally:
    driver.quit()  # Ensure that the WebDriver instance is closed properly
