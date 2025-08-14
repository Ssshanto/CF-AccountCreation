import csv

input_file = 'Accounts.csv'
output_file = 'Accounts_fixed.csv'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for i, row in enumerate(reader):
        if i == 0:
            # Write header as is
            writer.writerow(row)
        else:
            # Reconstruct the line to handle embedded commas in username
            line = ','.join(row)
            password = line[-12:]
            rest = line[:-12]
            # Split rest by comma, but only for the first 2 commas
            parts = rest.split(',', 2)
            if len(parts) == 3:
                id_, section, username = parts
                username = username.rstrip(',').strip('"')  # Remove trailing comma and extra quotes
            else:
                print(f"Skipping malformed row: {row}")
                continue
            writer.writerow([id_, section, username, password])

print(f"Fixed CSV written to {output_file}") 