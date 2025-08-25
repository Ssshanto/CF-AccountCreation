import time
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

def change_password(username, old_password, new_password, team_name=None):
    """
    Changes the password of a Codeforces account and optionally updates the team name.
    
    Args:
        username (str): The handle/username of the account
        old_password (str): The current password
        new_password (str): The new password to set
        team_name (str, optional): New team name to set if provided
    
    Returns:
        bool: True if password change was successful, False otherwise
    """
    try:
        # Set up Chrome driver
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        
        wait_for_x("Navigate to Codeforces login page")
        driver.get('https://codeforces.com/enter?')
        
        wait_for_x("Fill login credentials")
        try:
            # Find and fill the Handle/Email field
            handle_field = driver.find_element(By.NAME, 'handleOrEmail')
            handle_field.clear()
            handle_field.send_keys(username)
            print(f"Filled 'handleOrEmail' field with '{username}'")
            
            # Find and fill the Password field
            password_field = driver.find_element(By.NAME, 'password')
            password_field.clear()
            password_field.send_keys(old_password)
            print(f"Filled 'password' field")
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
        
        # Check if login was successful by looking for profile elements
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'logout')]"))
            )
            print("Login successful.")
        except TimeoutException:
            print("Login failed or timed out.")
            return False
        
        wait_for_x("Navigate to settings/general page")
        driver.get('https://codeforces.com/settings/general')
        
        wait_for_x("Fill password change fields")
        try:
            # Find and fill the Old password field
            old_password_field = driver.find_element(By.NAME, 'oldPassword')
            old_password_field.clear()
            old_password_field.send_keys(old_password)
            print(f"Filled 'oldPassword' field")
            
            # Find and fill the New password field
            new_password_field = driver.find_element(By.NAME, 'newPassword')
            new_password_field.clear()
            new_password_field.send_keys(new_password)
            print(f"Filled 'newPassword' field")
            
            # Find and fill the Confirm new password field
            confirm_password_field = driver.find_element(By.NAME, 'newPasswordConfirmation')
            confirm_password_field.clear()
            confirm_password_field.send_keys(new_password)
            print(f"Filled 'newPasswordConfirmation' field")
        except NoSuchElementException as e:
            print(f"Could not find password change field: {e}")
            return False
        
        wait_for_x("Click Save Changes button")
        try:
            save_btn = driver.find_element(By.XPATH, "//input[@class='submit' and @type='submit' and @value='Save changes']")
            save_btn.click()
            print("Clicked the Save Changes button.")
        except NoSuchElementException:
            print("Could not find the Save Changes submit button.")
            return False
        
        # Wait for password change to process
        time.sleep(3)
        
        # If team_name is provided, change the team name
        if team_name:
            wait_for_x("Navigate to create team page to change team name")
            driver.get('https://codeforces.com/teams/new')
            
            try:
                # Fill the englishName input with the new team name
                english_name_field = driver.find_element(By.NAME, 'englishName')
                english_name_field.clear()
                english_name_field.send_keys(team_name)
                print(f"Filled 'englishName' field with '{team_name}'")
                
                wait_for_x("Click the Create team submit button")
                create_team_btn = driver.find_element(By.XPATH, "//input[@class='submit create-team' and @type='submit' and @value='Create team']")
                create_team_btn.click()
                print("Clicked the Create team button.")
            except NoSuchElementException as e:
                print(f"Could not find team creation field or button: {e}")
                # Don't return False here as password change might have succeeded
        
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
        
        print(f"Password change completed successfully for user '{username}'")
        if team_name:
            print(f"Team name updated to '{team_name}'")
        
        return True
        
    except Exception as e:
        print(f"An error occurred during password change: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    # Example usage
    change_password("algo22_tmp_0000", "|5h#XF>V'D!c", "hehehe123", "Dum dum team")
    pass
