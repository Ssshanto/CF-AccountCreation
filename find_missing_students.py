import csv

accounts_file = 'Accounts.csv'
students_file = 'Students_List.csv'

# Read IDs from Accounts.csv (first column, skip header)
with open(accounts_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    account_ids = {row[0].strip() for row in reader if row}

# Read IDs from Students_List.csv (first column, skip header if present)
with open(students_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    students_ids = []
    for row in reader:
        if row and row[0].strip().isdigit():  # assuming IDs are numeric
            students_ids.append(row[0].strip())

missing_ids = [sid for sid in students_ids if sid not in account_ids]

print("Missing student IDs:")
print(missing_ids) 