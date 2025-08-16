
# Import required modules and project components

import logging
from src.scraper import search_linkedin_profiles, visit_and_extract_profile
from src.llm import verify_with_llm
from src.io_utils import load_input_data, save_verified_profiles
import config.config as config
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set up and return a Selenium Chrome WebDriver with custom options
def setup_driver():
    driver_path = chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('start-maximized')
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

# Main workflow to orchestrate the LinkedIn profile verification process
def run_workflow():
    # Set up logging format and level
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    # Load input data from CSV
    df = load_input_data()
    if df is None:
        return

    # Initialize Selenium WebDriver
    try:
        driver = setup_driver()
    except Exception as e:
        logging.error(f"Failed to initialize Chrome WebDriver: {e}")
        return

    verified_profiles = []  # List to store verified profiles

    # Iterate through each row in the input DataFrame
    for idx, row in df.iterrows():
        try:
            # Extract required fields from the row
            name = row[config.NAME_COL]
            company = row[config.COMPANY_COL]
            role = row[config.ROLE_COL]
        except Exception as e:
            logging.warning(f"Missing expected columns in row {idx}: {e}")
            continue

        # Search for LinkedIn profile links using Google
        links = search_linkedin_profiles(driver, name, company)

        # Visit each found LinkedIn profile and verify with LLM
        for link in links:
            # Scrape main and profile text from the LinkedIn page
            main_text, profile_text = visit_and_extract_profile(driver, link)

            # Use LLM to verify if the profile matches the person
            answer = verify_with_llm(name, company, main_text, profile_text)
            if answer.startswith('YES'):
                # If verified, add to the results and stop checking other links for this person
                verified_profiles.append({'Name': name, 'Company': company, 'LinkedIn': link})
                break

    # Close the browser
    driver.quit()

    # Save the verified profiles to output CSV
    save_verified_profiles(verified_profiles)
