import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
)
from cf_account_utils import *

def wait_for_x(step_name):
    print(f"\n[STEP] {step_name}")
    
    return

def automate_account_creation(driver, temp_id, student_details):
    try:
        wait_for_x("Open Codeforces registration page")
        driver.get('https://codeforces.com/register/')

        # Generate values
        username = generate_temp_username(temp_id)
        email = get_temp_email()
        password = generate_strong_password()

        wait_for_x("Fill all registration fields with generated values")
        field_values = {
            'handle': username,
            'email': email.email,
            'password': password,
            'passwordConfirmation': password,
        }
        for name, value in field_values.items():
            try:
                field = driver.find_element(By.NAME, name)
                field.clear()
                field.send_keys(value)
                print(f"Filled field '{name}' with '{value}'")
            except NoSuchElementException:
                print(f"Could not find field '{name}'")

        wait_for_x("Click the Register submit button")
        try:
            submit_btn = driver.find_element(By.XPATH, "//input[@class='submit' and @type='submit' and @value='Register']")
            submit_btn.click()
            print("Clicked the Register button.")
        except NoSuchElementException:
            print("Could not find the Register submit button.")

        wait_for_x("Print registration link from email inbox")

        while True:
            try:
                print(email.get_inbox())
                registration_link = get_registration_link(email.get_mail_content(mail_id=email.get_inbox()[0]['id']))
                print(f"Registration Link: {registration_link}")
                break
            except:                
                print("Waiting for email...")
                time.sleep(2)

        # Removed CSV writing logic here

        wait_for_x("Open the registration link URL")
        driver.get(registration_link)

        wait_for_x("Open the create team page")
        driver.get('https://codeforces.com/teams/new')

        # Fill the englishName input with the team name from student_details
        try:
            english_name_field = driver.find_element(By.NAME, 'englishName')
            english_name_field.clear()
            english_name_field.send_keys(student_details)
            print(f"Filled 'englishName' field with '{student_details}'")
        except NoSuchElementException:
            print("Could not find the 'englishName' field.")

        wait_for_x("Click the Create team submit button")
        try:
            create_team_btn = driver.find_element(By.XPATH, "//input[@class='submit create-team' and @type='submit' and @value='Create team']")
            create_team_btn.click()
            print("Clicked the Create team button.")
        except NoSuchElementException:
            print("Could not find the Create team submit button.")

        wait_for_x("Logout from the account")
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                logout_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'logout') and contains(., 'Logout')]") )
                )
                logout_link.click()
                print("Clicked the Logout button.")
                break
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                print(f"Attempt {attempt+1}: {type(e).__name__} - retrying...")
                time.sleep(1)
            except TimeoutException:
                print("Timed out waiting for the Logout button to become clickable.")
                break
            except NoSuchElementException:
                print("Could not find the Logout button.")
                break

        return username, password
    finally:
        driver.quit()
    
