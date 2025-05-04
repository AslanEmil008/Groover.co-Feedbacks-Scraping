from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Initialize the WebDriver for Firefox
driver = webdriver.Firefox()

# Open the Groover website
driver.get("https://groover.co/en/")

# Wait for the page to load
time.sleep(2)

# Wait for the login button and ensure it's clickable
login_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test-id='loginLink']"))
)

# Scroll the login button into view
driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
time.sleep(1)  # Give it a moment to ensure the button is fully in view

# Click the login button using JavaScript if normal click doesn't work
driver.execute_script("arguments[0].click();", login_button)

# Wait for the login page to load
time.sleep(2)

# Enter email and password
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-id='loginFormEmailInputField']"))
)
email_input.send_keys("your-email@gmail.com")  # Replace with your email

time.sleep(2)

password_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='loginFormPasswordInputField']")
password_input.send_keys("your-password")  # Replace with your password

time.sleep(2)

# Press Enter to log in
password_input.send_keys(Keys.RETURN)

# Wait for the login to process
time.sleep(5)

# Click on "My Campaigns"
my_campaigns_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-test-id='bandTopNavigationCampaignsCTA']"))
)
my_campaigns_button.click()

# Wait for the page with the songs to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "span.tw-ellipsis"))
)

# Scroll down to ensure all elements are loaded (if there are many song names)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  # Allow time for new content to load

# Find all song names by targeting specific elements within the campaign sections
song_names = driver.find_elements(By.CSS_SELECTOR, "div.layoutTemplateContainer span.tw-ellipsis")

# Filter out unwanted song names
valid_song_names = []
for song in song_names:
    song_name = song.text.strip()

    # Filter out unwanted values
    if song_name not in ["Send new track", "My email list", "All responses"] and song_name:
        valid_song_names.append(song_name)

# Save valid song names to CSV
with open("song_names.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Song Name"])  # Write header
    for song in valid_song_names:
        writer.writerow([song])  # Write each song name to the CSV

# Close the browser
driver.quit()
