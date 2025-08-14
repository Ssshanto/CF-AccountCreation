from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from account_creation import automate_account_creation
from cf_account_utils import get_student, get_missing_students
import random
import string
import csv

if __name__ == "__main__":
    
    # missing_students = ['220041124', '220041128', '220041137', '220041144', '220041145', '220041159', '220041164', '220041223', '220041233', '220041240', '220041241']
    # print(len(missing_students))
    
    # for account_index in range(10, 11):
    #     print(f"Processing account {account_index}")
        
    #     chrome_options = Options()
    #     chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #     driver = webdriver.Chrome(options=chrome_options)
        
    #     suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

    #     id, name, section = get_missing_students(missing_students[account_index])
    #     student_details = f"{id}, {name}"
    #     print(f"Student Details: {student_details}")
    #     username, password = automate_account_creation(driver, suffix, student_details)
    #     print(id, section, username, password, student_details)
    #     with open('Accounts.csv', 'a') as f:
    #         f.write(f"{id},{section},{username},{password}\n")

    for account_index in range(10):
        print(f"Processing account {account_index}")
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=chrome_options)
        
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

        id, name, section = "Dummy", "Dummy", "Dummy"
        student_details = f"Dummy Account"
        print(f"Student Details: {student_details}")
        username, password = automate_account_creation(driver, suffix, student_details)
        print(id, section, username, password, student_details)
        with open('Accounts.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([id, section, username, password])
