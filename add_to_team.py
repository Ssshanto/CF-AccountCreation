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


def add_to_team(username, password, added_user):
    """
    Logs into Codeforces, navigates to the teams page, opens the second team's edit page,
    appends that URL to 'old_teams_links.csv', invites a user to the team, and logs out.

    Args:
        username (str): Codeforces handle or email
        password (str): Codeforces password
        added_user (str): Handle to invite to the team

    Returns:
        bool: True if the flow completes through inviting and logout, False otherwise
    """

    driver = None
    try:
        # Set up Chrome driver to attach to an existing debugging session (consistent with change_password.py)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)

        # 1) Login
        wait_for_x("Navigate to Codeforces login page")
        driver.get('https://codeforces.com/enter?')

        wait_for_x("Fill login credentials")
        try:
            handle_field = driver.find_element(By.NAME, 'handleOrEmail')
            handle_field.clear()
            handle_field.send_keys(username)
            print(f"Filled 'handleOrEmail' field with '{username}'")

            password_field = driver.find_element(By.NAME, 'password')
            password_field.clear()
            password_field.send_keys(password)
            print("Filled 'password' field")
        except NoSuchElementException as e:
            print(f"Could not find login field: {e}")
            return False

        wait_for_x("Click the Login submit button")
        try:
            submit_btn = driver.find_element(By.XPATH, "//input[@class='submit' and @type='submit' and @value='Login']")
            submit_btn.click()
            print("Clicked the Login button.")
        except NoSuchElementException:
            print("Could not find the Login submit button.")
            return False

        # Wait for login to complete
        time.sleep(3)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'logout')]"))
            )
            print("Login successful.")
        except TimeoutException:
            print("Login failed or timed out.")
            return False

        # 2) Open the Teams page
        wait_for_x("Open Codeforces teams page")
        driver.get('https://codeforces.com/teams')

        # 3) Click the SECOND edit icon and append the loaded URL to 'old_teams_links.csv'
        wait_for_x("Click the second Edit icon for teams")
        try:
            edit_icons = driver.find_elements(
                By.XPATH,
                "//img[@src='//codeforces.org/s/56867/images/actions/edit.png' and @alt='Edit' and @title='Edit']"
            )
            if len(edit_icons) < 2:
                print("Less than two edit icons found on the teams page.")
                return False
            # Click the second edit icon
            edit_icons[1].click()
            print("Clicked the second Edit icon.")

            # Wait for navigation to the team edit/manage page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Invite user']"))
            )

            # Append the current URL to CSV
            current_url = driver.current_url
            print(f"Team edit page URL: {current_url}")
            try:
                with open('old_teams_links.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([current_url])
                print("Appended edit page URL to 'old_teams_links.csv'.")
            except Exception as e:
                print(f"Failed to write URL to 'old_teams_links.csv': {e}")
                # Continue even if CSV write fails
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Could not click the second Edit icon or navigate to edit page: {e}")
            return False

        # 4) Click the "Invite user" link
        wait_for_x("Open the Invite user dialog/section")
        try:
            invite_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Invite user']"))
            )
            invite_link.click()
            print("Clicked 'Invite user'.")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Could not open 'Invite user' section: {e}")
            return False

        # 5) Type the added_user into the 'customHandle' input
        wait_for_x("Fill invite handle field")
        try:
            handle_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'customHandle'))
            )
            handle_input.clear()
            handle_input.send_keys(added_user)
            print(f"Filled 'customHandle' with '{added_user}'.")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Could not find the 'customHandle' input: {e}")
            return False

        # 6) Click the Invite button
        wait_for_x("Click Invite submit button")
        try:
            invite_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Invite']"))
            )
            invite_button.click()
            print("Clicked the Invite button.")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Could not find or click the Invite button: {e}")
            return False

        # Optionally wait a bit for the action
        time.sleep(2)

        # 7) Logout
        wait_for_x("Logout from the account")
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                logout_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'logout') and contains(., 'Logout')]"))
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

        return True

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    # Dummy invocation for testing
    # Note: This expects Chrome to be running with --remote-debugging-port=9222
    # and a valid Codeforces session context. Replace with valid credentials to test.
    add_to_team("algo22_tmp_PTS2", "S9Wdo%F34F", "ssshanto")
