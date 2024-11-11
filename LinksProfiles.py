from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import signal
import sys
import html  # Import html module to handle HTML entities

# Initialize the WebDriver for Firefox
driver = webdriver.Firefox()

# Open the Groover website
driver.get("https://groover.co/en/")

# Wait for the page to load
time.sleep(2)

# Click the login button using CSS Selector
login_button_css = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='loginLink']")
login_button_css.click()

# Wait for the login page to load
time.sleep(2)

# Enter email and password
email_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='loginFormEmailInputField']")
email_input.send_keys("aspenjadeartist@gmail.com")  # Replace with your email

password_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='loginFormPasswordInputField']")
password_input.send_keys("Scrapy*11")  # Replace with your password

# Press Enter to log in
password_input.send_keys(Keys.RETURN)

# Clicking login button
login_submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='loginFormSubmitCTA']")
login_submit_button.click()
time.sleep(5)

# Navigate to "My Campaigns"
my_campaigns_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='bandTopNavigationCampaignsCTA']"))
)
my_campaigns_link.click()

time.sleep(5)

# Finding the specific song and clicking it for feedback scraping
obsessed_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Before']"))
    #[Before,BEFORE,Obsessed,INFINITE,Searching,Alternate Universes,Infinite]
)
obsessed_element.click()

# Wait for the influencers to load
time.sleep(5)

# List to store the profiles
profiles_data = []
visited_names = set()  # Set to keep track of processed influencer names

# Function to save profiles to CSV
# Change CSV filename per song if necessary
def save_to_csv(profiles, filename='influencer_profiles_Before.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "link"])
        writer.writeheader()
        writer.writerows(profiles)
    print(f"Saved {len(profiles)} profiles to {filename}.")

# Function to handle termination
def signal_handler(sig, frame):
    print("\nTermination signal received.")
    save_to_csv(profiles_data)  # Save before exit
    driver.quit()  # Ensure the driver is closed
    sys.exit(0)  # Exit the script

# Set up signal handling
signal.signal(signal.SIGINT, signal_handler)

# Function to check and click the "Next Page" button
def go_to_next_page():
    try:
        # Wait for the "Next Page" button to become clickable
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Next Page']"))
        )
        # Check if the button is disabled (i.e., no more pages)
        if "disabled" in next_page_button.get_attribute("class"):
            print("No more pages to navigate.")
            return False  # No more pages, stop scraping
        else:
            # Click the "Next Page" button
            next_page_button.click()
            time.sleep(3)  # Wait for the next page to load
            return True  # Proceed to next page
    except Exception as e:
        print(f"Error while trying to go to the next page: {e}")
        return False  # Stop scraping if an error occurs

try:
    # Start pagination loop
    while True:
        # Wait until influencer names are present
        name_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'desktopDisplay')]//span[contains(@class, 'tw-ellipsis') and not(contains(., 'Add optional files')) and not(contains(., 'Add the requested files'))]")
            )
        )

        # Loop through the filtered influencer name elements
        for influencer_name_element in name_elements:
            influencer_name = influencer_name_element.text  # Get the name of the influencer

            # Decode HTML entities and clean up any surrounding spaces or special characters
            influencer_name = html.unescape(influencer_name).strip()
            
            # Remove any trailing or leading spaces or semicolons
            influencer_name = influencer_name.replace(' ;', '').strip()  # Adjust based on your data

            # Skip if this influencer has already been processed
            if influencer_name in visited_names:
                continue

            print(f"Clicking on influencer: {influencer_name}")  # Print the name being clicked

            # Click the influencer to navigate to their profile
            influencer_name_element.click()

            # Wait for the profile page to load
            time.sleep(3)  # Adjust time as necessary

            # Initialize profile_link to None
            profile_link = ""

            try:
                # Scrape the link to the influencer's profile
                profile_link_element = driver.find_element(By.CSS_SELECTOR, "a[data-v-67f8ff01]")
                profile_link = profile_link_element.get_attribute("href")  # Get the URL from the anchor tag
                
                # Check if profile_link is None
                if not profile_link:
                    print(f"No link for {influencer_name}.")  # Print no link message
                    profile_link = ""  # Ensure it's an empty string for CSV

            except Exception:
                print(f"No link for {influencer_name}.")  # Print no link message

            # Store the data
            profiles_data.append({"name": influencer_name, "link": profile_link})
            visited_names.add(influencer_name)  # Mark this name as visited

            # Save to CSV after each successful scrape
            save_to_csv(profiles_data)

            # Go back to the previous page to click the next influencer
            driver.back()
            time.sleep(3)  # Wait for the previous page to load again

        # Now go to the next page, if possible
        if not go_to_next_page():
            break  # Exit the loop if no more pages or an error occurred

except Exception as e:
    print(f"An error occurred: {str(e)}")
    save_to_csv(profiles_data)  # Save before exit

finally:
    # Final save in case the script exits without a signal
    save_to_csv(profiles_data)

    # Close the driver
    driver.quit()





