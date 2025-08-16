
# Handles all Selenium-based web scraping and navigation
import time
import random
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Handle Google consent/terms pop-up if present
def handle_google_consent(driver):
    while True:
        if 'consent' in driver.current_url or 'before you continue' in driver.page_source.lower():
            logging.info("Please review and accept Google's terms in the browser window. Press Enter here when you see the search box.")
            input()
            driver.refresh()
        else:
            break

# Handle LinkedIn login prompt if present
def handle_linkedin_login(driver):
    while True:
        if 'login' in driver.current_url or 'sign in' in driver.page_source.lower():
            logging.info("Please log in to LinkedIn in the browser window. Press Enter here when the profile page is visible.")
            input()
            driver.refresh()
        else:
            break

# Search Google for LinkedIn profile links for a given name and company
def search_linkedin_profiles(driver, name, company):
    query = f'{name} {company} "LinkedIn"'
    try:
        driver.get('https://www.google.com')
    except Exception as e:
        logging.error(f"Failed to load Google: {e}")
        return []
    handle_google_consent(driver)
    try:
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, 'q')))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
    except Exception as e:
        logging.error(f"Failed to perform Google search: {e}")
        return []
    if 'sorry/index' in driver.current_url or 'captcha' in driver.page_source.lower():
        logging.warning("CAPTCHA detected! Please solve the CAPTCHA in the browser window. Press Enter here when done...")
        input()
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if 'linkedin.com/in/' in a['href']]
        return list(set(links))
    except Exception as e:
        logging.error(f"Failed to parse Google results: {e}")
        return []

# Visit a LinkedIn profile link and extract main and profile text
def visit_and_extract_profile(driver, link):
    try:
        driver.get(link)
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        logging.error(f"Failed to load LinkedIn profile: {e}")
        return '', ''
    handle_linkedin_login(driver)
    # Ensure the correct profile link is loaded after login
    if not driver.current_url.startswith(link):
        try:
            driver.get(link)
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            logging.error(f"Failed to reload LinkedIn profile after login: {e}")
            return '', ''
    try:
        main_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[@class = 'mt2 relative']"
            ))
        )
        main_text = main_elem.text.strip()
    except Exception as e:
        logging.warning(f"Could not locate main card: {e}")
        main_text = ''
    try:
        section_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//section["
                "contains(@class, 'artdeco-card') and "
                "contains(@class, 'pv-profile-card') and "
                "contains(@class, 'break-words') and "
                ".//span[text() = 'Experience']"
                "]"
            ))
        )
        profile_text = section_elem.text.strip()
    except Exception as e:
        logging.warning(f"Could not locate main profile section: {e}")
        profile_text = ''
    return main_text, profile_text
