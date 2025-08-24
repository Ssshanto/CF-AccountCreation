from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from account_creation import automate_account_creation
from cf_account_utils import get_student, get_missing_students, generate_strong_password
from change_password import change_password
import random
import string
import csv
import pandas as pd

if __name__ == "__main__":
    
    # Previous logic - commented out
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

    # for account_index in range(10):
    #     print(f"Processing account {account_index}")
        
    #     chrome_options = Options()
    #     chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #     driver = webdriver.Chrome(options=chrome_options)
        
    #     suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

    #     id, name, section = "Dummy", "Dummy", "Dummy"
    #     student_details = f"Dummy Account"
    #     print(f"Student Details: {student_details}")
    #     username, password = automate_account_creation(driver, suffix, student_details)
    #     print(id, section, username, password, student_details)
    #     with open('Accounts.csv', 'a', newline='', encoding='utf-8') as f:
    #         writer = csv.writer(f)
    #         writer.writerow([id, section, username, password])

    # New logic for password changing with Students_List.csv integration
    try:
        # Load existing Accounts.csv to get already processed data
        existing_accounts = set()
        existing_student_ids = set()
        
        try:
            accounts_df = pd.read_csv('Accounts.csv')
            if not accounts_df.empty:
                existing_accounts = set(accounts_df['Username'].tolist())
                existing_student_ids = set(accounts_df['ID'].astype(str).tolist())
                print(f"Found {len(existing_accounts)} existing accounts and {len(existing_student_ids)} processed student IDs in Accounts.csv")
            else:
                print("Accounts.csv is empty, will process all accounts and students")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print("Accounts.csv not found or empty, will process all accounts and students")
        
        # Load the Students_List.csv file
        students_df = pd.read_csv('Students_List.csv')
        print(f"Loaded {len(students_df)} students from Students_List.csv")
        
        # Filter out students that are already processed
        students_df['ID'] = students_df['ID'].astype(str)
        unprocessed_students_df = students_df[~students_df['ID'].isin(existing_student_ids)]
        print(f"Found {len(unprocessed_students_df)} unprocessed students")
        
        # Convert students data to list of dictionaries for easier manipulation
        students_list = unprocessed_students_df.to_dict('records')
        
        # Load the credentials from .xlsx file
        credentials_df = pd.read_excel('Old_Credentials.xlsx')
        
        # Filter out accounts that are already processed
        unprocessed_credentials_df = credentials_df[~credentials_df['username'].isin(existing_accounts)]
        print(f"Found {len(unprocessed_credentials_df)} unprocessed accounts from Old_Credentials.xlsx")
        
        # Get username and password columns for unprocessed accounts
        usernames = unprocessed_credentials_df['username'].tolist()
        old_passwords = unprocessed_credentials_df['password'].tolist()
        
        # Create credentials list
        credentials_list = list(zip(usernames, old_passwords))
        
        # Check if we have enough accounts for all students
        if len(credentials_list) < len(students_list):
            print(f"Warning: Only {len(credentials_list)} unprocessed accounts available for {len(students_list)} unprocessed students")
            print("Will process only the number of students that can be matched with available accounts")
            students_list = students_list[:len(credentials_list)]
        elif len(students_list) < len(credentials_list):
            print(f"Note: {len(credentials_list)} accounts available for {len(students_list)} students")
            credentials_list = credentials_list[:len(students_list)]
        
        # Skip processing if no unprocessed data
        if not students_list or not credentials_list:
            print("No unprocessed students or accounts found. All processing appears to be complete.")
        else:
            # Randomly shuffle both lists
            random.shuffle(students_list)
            random.shuffle(credentials_list)
            
            print(f"Shuffled {len(students_list)} unprocessed students and {len(credentials_list)} unprocessed accounts")
            
            # Write header to Accounts.csv if file doesn't exist or is empty
            try:
                with open('Accounts.csv', 'r') as f:
                    first_line = f.readline().strip()
                    if not first_line:
                        write_header = True
                    else:
                        write_header = False
            except FileNotFoundError:
                write_header = True
            
            if write_header:
                with open('Accounts.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Lab_Section', 'Username', 'Password'])
            
            # Process each unprocessed student with corresponding unprocessed credentials
            for index, (student, (username, old_password)) in enumerate(zip(students_list, credentials_list)):
                student_id = str(student['ID'])
                nickname = student['Nickname']
                lab_section = student['Lab Section']
                
                print(f"\nProcessing student {index + 1}/{len(students_list)}: {student_id} - {nickname}")
                
                # Generate new password
                new_password = generate_strong_password(10)
                print(f"Generated new password for {username}")
                
                # Set team_name as requested: f'{Nickname}, {ID}'
                team_name = f'{nickname}, {student_id}'
                print(f"Team name: {team_name}")
                
                # Apply change_password logic
                success = change_password(username, old_password, new_password, team_name)
                
                if success:
                    print(f"Password changed successfully for {username}")
                    
                    # Store username, new_password, ID, Lab Section in Accounts.csv
                    with open('Accounts.csv', 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([student_id, lab_section, username, new_password])
                    print(f"Saved new credentials for {username} (Student: {student_id}) to Accounts.csv")
                else:
                    print(f"Failed to change password for {username}")
            
            print(f"\nCompleted processing {len(students_list)} unprocessed students from Students_List.csv")
            
    except FileNotFoundError as e:
        print(f"Error: Required file not found - {e}")
    except Exception as e:
        print(f"Error: {e}")
