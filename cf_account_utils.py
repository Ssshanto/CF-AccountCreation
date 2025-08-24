import random
import string
from temp_mails import Tenminemail_com
from bs4 import BeautifulSoup
import re
import csv

username_prefix = 'algo22_tmp'

def generate_temp_username(suffix) -> str:
    return f"{username_prefix}_{suffix}"

def generate_strong_password(length: int = 8) -> str:
    allowed_punctuations = '@&%#'
    chars = string.ascii_letters + string.digits + allowed_punctuations
    # Ensure at least one character from each category
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(allowed_punctuations),
    ]
    if length < 4:
        raise ValueError("Password length must be at least 4")
    password += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(password)
    return ''.join(password)

def get_temp_email():
    mail = Tenminemail_com()
    return mail

def get_registration_link(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    # Find the specific link using a regular expression
    confirmation_link_tag = soup.find('a', href=re.compile(r'https://codeforces.com/register/confirm/'))

    if confirmation_link_tag:
        confirmation_link = confirmation_link_tag['href']
        return confirmation_link
    else:
        print("Failed to fetch registration link")
        return -1
    

def get_student(index):
    with open('Students_List.csv', 'r') as f:
        lines = f.readlines()
        if index + 1 >= len(lines):
            return None
        values = lines[index + 1].strip().split(',')
        return values[0], values[2], values[3]

def get_missing_students(id):
    with open('Students_List.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for values in reader:
            if values and values[0].strip() == str(id):
                # Return ID, 3rd, and 4th columns
                return values[0], values[2], values[3]
    return None  # If not found

if __name__ == '__main__':
    # Example usage
    print(generate_strong_password(10))