# CF Account Creation

Automated script for creating Codeforces accounts and teams.

## Setup

1. Install required packages:
```bash
pip install selenium beautifulsoup4 lxml temp_mails openpyxl
```

2. Launch Chrome with remote debugging:
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug_temp"
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. The script will:
   - Create Codeforces accounts for students
   - Generate teams
   - Save account details to `Accounts.csv`

## Files

- `main.py` - Main execution script
- `account_creation.py` - Account creation automation
- `cf_account_utils.py` - Utility functions
- `Accounts.csv` - Generated account details
- `Students_List.csv` - Student information

## Notes

- Ensure Chrome is running with debugging enabled before running the script
- The script will pause at each step - press 'X' and Enter to continue
- Account details are automatically saved to CSV format 