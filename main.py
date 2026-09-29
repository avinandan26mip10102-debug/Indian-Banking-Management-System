"""
main.py - Main Program Driver and Terminal Menu Interface
Course: Python Essentials (First-Year Student Academic Project)

Student Explanation:
This is the main driver program for our Indian Banking Management System.
It imports functions and classes from the other 5 modules:
  1. constants.py
  2. validators.py
  3. security_tools.py
  4. calculations.py
  5. bank_account.py
It presents an interactive menu-driven interface using a while True loop,
routing user actions cleanly to appropriate screen functions.
"""

from constants import (
    ALLOWED_ACCOUNT_TYPES,
    VALID_BRANCH_CODES,
    MIN_BALANCE_SAVINGS,
    MIN_BALANCE_CURRENT,
    SERVICE_FLAG_NET_BANKING,
    SERVICE_FLAG_ATM_CARD,
    SERVICE_FLAG_SMS_ALERTS,
    SERVICE_FLAG_CHEQUE_BOOK
)
from validators import (
    is_only_digits,
    is_valid_rupee_amount,
    is_valid_indian_phone,
    is_valid_applicant_age,
    is_valid_ifsc_branch
)
from security_tools import toggle_service_permission
from calculations import (
    compute_simple_interest,
    compute_compound_interest,
    compute_monthly_average,
    get_cash_notes_breakdown
)
from bank_account import BankAccount, setup_initial_bank_data


# ============================================================================
# USER INTERACTION SCREENS / HANDLER FUNCTIONS
# ============================================================================

def open_account_view(accounts_db, registered_mobiles):
    """
    Screen 1: Opens a new bank account after gathering and validating user inputs.
    Demonstrates:
    - input() and print()
    - Control flow (if-elif-else, nested conditions)
    - Membership operators ('in', 'not in')
    - Type conversions: int(), float(), str()
    - Adding to Dictionary and Set
    """
    print("\n" + "=" * 52)
    print("             OPEN NEW BANK ACCOUNT")
    print("=" * 52)

    # 1. Customer Name Input
    full_name = input("Enter Full Name of Customer: ").strip()
    if len(full_name) == 0:
        print("Validation Error: Customer name cannot be empty.")
        return

    # 2. Age Input & Validation
    age_str = input("Enter Age (18 to 100): ").strip()
    if not is_only_digits(age_str):
        print("Validation Error: Age must be a positive whole number.")
        return
    age = int(age_str)
    if not is_valid_applicant_age(age):
        print("Validation Error: Customer must be an adult between 18 and 100 years of age.")
        return

    # 3. Mobile Number Input & Validation
    mobile_input = input("Enter 10-digit Indian Mobile Number: ").strip()
    if not is_valid_indian_phone(mobile_input):
        print("Validation Error: Mobile number must have exactly 10 digits starting with 6, 7, 8, or 9.")
        return
    # Membership check in set
    if mobile_input in registered_mobiles:
        print("Validation Error: This mobile number is already linked to another registered bank account.")
        return

    # 4. Account Type Selection (Checked against tuple)
    print("\nAccount Types Available:")
    print("  1. Savings Account (Personal savings, min balance Rs. 500)")
    print("  2. Current Account (Business account, min balance Rs. 1000)")
    type_choice = input("Select Account Type (1 or 2): ").strip()

    if type_choice == "1":
        chosen_type = ALLOWED_ACCOUNT_TYPES[0]
        min_deposit = MIN_BALANCE_SAVINGS
    elif type_choice == "2":
        chosen_type = ALLOWED_ACCOUNT_TYPES[1]
        min_deposit = MIN_BALANCE_CURRENT
    else:
        print("Validation Error: Invalid account type selected. Account creation aborted.")
        return

    # 5. Branch Code Selection (Checked against frozenset)
    available_branches_list = sorted(list(VALID_BRANCH_CODES))
    print("\nAuthorized Bank Branch Codes: " + ", ".join(available_branches_list))
    branch_code = input("Enter Branch Code (e.g., SBIN001): ").strip().upper()
    if not is_valid_ifsc_branch(branch_code):
        print("Validation Error: Invalid branch code! Must be an authorized IFSC code.")
        return

    # 6. Opening Initial Deposit
    deposit_str = input(f"Enter Opening Deposit (Minimum Rs. {min_deposit:.2f}): ").strip()
    if not is_valid_rupee_amount(deposit_str):
        print("Validation Error: Deposit amount must be a positive decimal number.")
        return
    initial_deposit = float(deposit_str)
    if initial_deposit < min_deposit:
        print(f"Validation Error: Opening deposit must be at least Rs. {min_deposit:.2f} for {chosen_type} accounts.")
        return

    # 7. Generate Sequential Account Number
    existing_account_numbers = list(accounts_db.keys())
    if len(existing_account_numbers) > 0:
        new_account_number = max(existing_account_numbers) + 1
    else:
        new_account_number = 1001

    # Instantiate BankAccount object (OOP)
    new_account = BankAccount(
        account_number=new_account_number,
        customer_name=full_name,
        age=age,
        mobile_number=mobile_input,
        account_type=chosen_type,
        initial_deposit=initial_deposit,
        branch_code=branch_code
    )

    # Store in memory: Dictionary and Set
    accounts_db[new_account_number] = new_account
    registered_mobiles.add(mobile_input)

    print("\n" + "*" * 52)
    print("SUCCESS: NEW ACCOUNT OPENED SUCCESSFULLY!")
    print(f"Account Holder : {full_name}")
    print(f"Account Number : {new_account_number}")
    print(f"Account Type   : {chosen_type}")
    print(f"Branch Code    : {branch_code}")
    print(f"Opening Balance: Rs. {initial_deposit:.2f}")
    print("*" * 52)


def view_account_view(accounts_db):
    """
    Screen 2: Displays full details of a specific account.
    Demonstrates: Dictionary key lookup and membership operator 'in'.
    """
    print("\n--- VIEW ACCOUNT DETAILS ---")
    acc_str = input("Enter Account Number to view: ").strip()
    if not is_only_digits(acc_str):
        print("Error: Account number must contain digits only.")
        return

    account_no = int(acc_str)
    if account_no in accounts_db:
        customer_acc = accounts_db[account_no]
        customer_acc.display_details()
    else:
        print(f"Error: Account #{account_no} does not exist in our banking records.")


def deposit_view(accounts_db):
    """
    Screen 3: Allows deposit of funds into an existing account.
    """
    print("\n--- DEPOSIT FUNDS ---")
    acc_str = input("Enter Account Number: ").strip()
    if not is_only_digits(acc_str):
        print("Error: Account number must be numeric.")
        return

    account_no = int(acc_str)
    if account_no not in accounts_db:
        print(f"Error: Account #{account_no} was not found.")
        return

    amount_str = input("Enter Amount to Deposit (Rs.): ").strip()
    if not is_valid_rupee_amount(amount_str):
        print("Error: Deposit amount must be a positive number.")
        return

    deposit_amount = float(amount_str)
    accounts_db[account_no].deposit(deposit_amount)


def withdraw_view(accounts_db):
    """
    Screen 4: Withdraws money with ATM cash denomination dispenser.
    """
    print("\n--- WITHDRAW CASH ---")
    acc_str = input("Enter Account Number: ").strip()
    if not is_only_digits(acc_str):
        print("Error: Account number must be numeric.")
        return

    account_no = int(acc_str)
    if account_no not in accounts_db:
        print(f"Error: Account #{account_no} was not found.")
        return

    amount_str = input("Enter Amount to Withdraw (Rs., multiple of 100): ").strip()
    if not is_valid_rupee_amount(amount_str):
        print("Error: Withdrawal amount must be a positive number.")
        return

    withdraw_amount = float(amount_str)
    success = accounts_db[account_no].withdraw(withdraw_amount)

    # Optional cash denomination breakdown demonstration
    if success:
        user_choice = input("Would you like to view the ATM currency note dispenser breakdown? (y/n): ").strip().lower()
        if user_choice == "y" or user_choice == "yes":
            dispenser_notes, leftover = get_cash_notes_breakdown(withdraw_amount)
            print("\nATM Currency Dispenser Output:")
            for note_value in dispenser_notes:
                count = dispenser_notes[note_value]
                print(f" - Rs. {note_value} currency notes : {count}")


def check_balance_view(accounts_db):
    """
    Screen 5: Checks account balance and shows simulated monthly average balance.
    Demonstrates mixed-type division (float / int = float).
    """
    print("\n--- CHECK ACCOUNT BALANCE ---")
    acc_str = input("Enter Account Number: ").strip()
    if not is_only_digits(acc_str):
        print("Error: Account number must be numeric.")
        return

    account_no = int(acc_str)
    if account_no not in accounts_db:
        print(f"Error: Account #{account_no} was not found.")
        return

    target_acc = accounts_db[account_no]
    current_bal = target_acc.check_balance()

    print(f"\nAccount #{target_acc.account_number} | Holder: {target_acc.customer_name}")
    print(f"Current Available Balance: Rs. {current_bal:.2f}")

    # Demonstrating mixed-type division from syllabus
    monthly_avg = compute_monthly_average(current_bal, 12)
    print(f"Simulated Monthly Average Balance (balance / 12): Rs. {monthly_avg:.2f}")


def transfer_view(accounts_db):
    """
    Screen 6: Transfers money between two accounts.
    Demonstrates identity operators ('is' and 'is not').
    """
    print("\n--- TRANSFER MONEY BETWEEN ACCOUNTS ---")
    sender_str = input("Enter Sender (Source) Account Number: ").strip()
    if not is_only_digits(sender_str):
        print("Error: Sender account number must be numeric.")
        return

    receiver_str = input("Enter Receiver (Destination) Account Number: ").strip()
    if not is_only_digits(receiver_str):
        print("Error: Receiver account number must be numeric.")
        return

    sender_no = int(sender_str)
    receiver_no = int(receiver_str)

    if sender_no not in accounts_db:
        print(f"Error: Sender Account #{sender_no} does not exist.")
        return

    if receiver_no not in accounts_db:
        print(f"Error: Receiver Account #{receiver_no} does not exist.")
        return

    sender_account = accounts_db[sender_no]
    receiver_account = accounts_db[receiver_no]

    # Identity operator check
    if sender_account is receiver_account:
        print("Error: Source and destination accounts cannot be the exact same account!")
        return

    amount_str = input("Enter Amount to Transfer (Rs.): ").strip()
    if not is_valid_rupee_amount(amount_str):
        print("Error: Transfer amount must be positive.")
        return

    transfer_amount = float(amount_str)
    sender_account.transfer_to(receiver_account, transfer_amount)


def display_all_accounts_view(accounts_db):
    """
    Screen 7: Displays all accounts in a formatted table.
    Demonstrates:
    - Converting dictionary values into a list
    - for loop iteration
    - Calculating totals and averages with arithmetic operators
    """
    print("\n" + "=" * 76)
    print("                     ALL REGISTERED BANK ACCOUNTS")
    print("=" * 76)

    # Convert dictionary values into a list data structure
    all_accounts_list = list(accounts_db.values())

    if len(all_accounts_list) == 0:
        print("No accounts are currently registered in the system.")
        print("=" * 76)
        return

    print(f"{'Acc No':<10}{'Customer Name':<22}{'Type':<12}{'Branch':<12}{'Balance (Rs.)':<15}")
    print("-" * 76)

    total_bank_reserves = 0.0

    for account in all_accounts_list:
        total_bank_reserves += account.balance
        print(f"{account.account_number:<10}{account.customer_name:<22}{account.account_type:<12}{account.branch_code:<12}{account.balance:<15.2f}")

    print("-" * 76)
    average_balance = total_bank_reserves / len(all_accounts_list)
    print(f"Total Bank Accounts Registered : {len(all_accounts_list)}")
    print(f"Total Bank Deposits in Trust  : Rs. {total_bank_reserves:.2f}")
    print(f"Average Balance per Account   : Rs. {average_balance:.2f}")
    print("=" * 76)


def search_account_view(accounts_db):
    """
    Screen 8: Searches for an account using multiple criteria.
    Demonstrates:
    - for loop with break and continue statements
    - Substring membership check ('in')
    - Logical NOT ('not')
    """
    print("\n--- SEARCH FOR AN ACCOUNT ---")
    print("  1. Search by Account Number")
    print("  2. Search by Customer Name")
    print("  3. Search by Mobile Phone Number")
    search_choice = input("Enter search option (1, 2, or 3): ").strip()

    accounts_list = list(accounts_db.values())
    match_found = False

    if search_choice == "1":
        acc_str = input("Enter Account Number to locate: ").strip()
        if not is_only_digits(acc_str):
            print("Error: Account number must be numeric.")
            return
        target_no = int(acc_str)
        # Search using a for loop and break
        for acc in accounts_list:
            if acc.account_number == target_no:
                acc.display_details()
                match_found = True
                break

    elif search_choice == "2":
        name_query = input("Enter Customer Name or partial name: ").strip().lower()
        if len(name_query) == 0:
            print("Error: Search query cannot be blank.")
            return
        # for loop using continue to skip non-matching accounts
        for acc in accounts_list:
            if name_query not in acc.customer_name.lower():
                continue
            acc.display_details()
            match_found = True

    elif search_choice == "3":
        mobile_query = input("Enter 10-digit Mobile Number: ").strip()
        for acc in accounts_list:
            if acc.mobile_number == mobile_query:
                acc.display_details()
                match_found = True
                break
    else:
        print("Error: Invalid search option entered.")
        return

    # Logical NOT check
    if not match_found:
        print("No matching bank account found.")


def update_info_view(accounts_db, registered_mobiles):
    """
    Screen 9: Updates customer profile or toggles service flags.
    Demonstrates:
    - Set operations (remove old mobile, add new mobile)
    - Bitwise XOR (^) to flip service status
    """
    print("\n--- UPDATE CUSTOMER INFORMATION & SERVICES ---")
    acc_str = input("Enter Account Number: ").strip()
    if not is_only_digits(acc_str):
        print("Error: Account number must be numeric.")
        return

    account_no = int(acc_str)
    if account_no not in accounts_db:
        print(f"Error: Account #{account_no} was not found.")
        return

    customer_acc = accounts_db[account_no]

    print(f"\nModifying Account #{customer_acc.account_number} ({customer_acc.customer_name})")
    print("  1. Update Customer Name")
    print("  2. Update Registered Mobile Number")
    print("  3. Toggle Banking Service (Net Banking / SMS / Cheque Book)")
    option = input("Enter choice (1, 2, or 3): ").strip()

    if option == "1":
        new_name = input("Enter Updated Legal Full Name: ").strip()
        if len(new_name) > 0:
            customer_acc.update_name(new_name)
            print("Success: Customer name successfully updated.")
        else:
            print("Error: Name cannot be blank.")

    elif option == "2":
        new_mobile = input("Enter New 10-digit Indian Mobile Number: ").strip()
        if not is_valid_indian_phone(new_mobile):
            print("Error: Invalid mobile number format.")
            return
        if new_mobile in registered_mobiles and new_mobile != customer_acc.mobile_number:
            print("Error: That mobile number is already taken by another registered customer.")
            return
        # Update set
        registered_mobiles.remove(customer_acc.mobile_number)
        registered_mobiles.add(new_mobile)
        customer_acc.update_phone(new_mobile)
        print("Success: Registered mobile number successfully updated.")

    elif option == "3":
        print("\nSelect Digital Banking Service to Toggle:")
        print("  1. Internet / Net Banking")
        print("  2. SMS Notifications & Alerts")
        print("  3. Cheque Book Facility")
        service_pick = input("Select service (1, 2, or 3): ").strip()

        if service_pick == "1":
            customer_acc.toggle_service(SERVICE_FLAG_NET_BANKING)
            print("Success: Internet Banking service status toggled.")
        elif service_pick == "2":
            customer_acc.toggle_service(SERVICE_FLAG_SMS_ALERTS)
            print("Success: SMS Alerts service status toggled.")
        elif service_pick == "3":
            customer_acc.toggle_service(SERVICE_FLAG_CHEQUE_BOOK)
            print("Success: Cheque Book service status toggled.")
        else:
            print("Error: Invalid service selection.")
    else:
        print("Error: Invalid update option.")


def interest_view(accounts_db):
    """
    Screen 10: Calculates simple and compound interest.
    Demonstrates:
    - Arithmetic operators: *, /, **, //, %
    - Operator precedence and associativity
    """
    print("\n--- CALCULATE INTEREST & FIXED DEPOSIT RETURNS ---")
    acc_str = input("Enter Account Number (or press Enter to use a custom principal): ").strip()

    principal_amount = 0.0
    if len(acc_str) > 0:
        if is_only_digits(acc_str) and int(acc_str) in accounts_db:
            acc_obj = accounts_db[int(acc_str)]
            principal_amount = acc_obj.balance
            print(f"Using current balance of Account #{acc_obj.account_number}: Rs. {principal_amount:.2f}")
        else:
            print("Account not found. Switching to manual principal entry.")
            acc_str = ""

    if len(acc_str) == 0:
        p_input = input("Enter Principal Amount (Rs.): ").strip()
        if not is_valid_rupee_amount(p_input):
            print("Error: Invalid principal amount.")
            return
        principal_amount = float(p_input)

    rate_input = input("Enter Annual Interest Rate in % (e.g. 4.0 for Savings, 7.0 for FD): ").strip()
    if not is_valid_rupee_amount(rate_input):
        print("Error: Invalid interest rate.")
        return
    annual_rate = float(rate_input)

    tenure_input = input("Enter Tenure in Months (e.g., 12, 24, 36): ").strip()
    if not is_only_digits(tenure_input):
        print("Error: Tenure months must be a positive integer.")
        return
    tenure_months = int(tenure_input)

    # Floor division and modulus operators
    tenure_years_whole = tenure_months // 12
    tenure_remaining_months = tenure_months % 12
    # True division
    tenure_in_years = tenure_months / 12.0

    print(f"\nTenure Breakdown: {tenure_years_whole} year(s) and {tenure_remaining_months} month(s) (Total {tenure_in_years:.2f} years)")

    # 1. Simple Interest calculation
    simple_int = compute_simple_interest(principal_amount, annual_rate, tenure_in_years)
    total_simple_value = principal_amount + simple_int

    # 2. Compound Interest calculation
    compound_int, maturity_compound_value = compute_compound_interest(principal_amount, annual_rate, tenure_in_years)

    print("\n" + "=" * 52)
    print("                INTEREST ESTIMATE")
    print("=" * 52)
    print(f"Principal Amount (P)    : Rs. {principal_amount:.2f}")
    print(f"Annual Rate (R)         : {annual_rate:.2f}% per annum")
    print(f"Duration (T)            : {tenure_in_years:.2f} years")
    print("-" * 52)
    print(f"1. Simple Interest (SI) : Rs. {simple_int:.2f}")
    print(f"   Maturity (P + SI)    : Rs. {total_simple_value:.2f}")
    print("-" * 52)
    print(f"2. Compound Interest    : Rs. {compound_int:.2f}")
    print(f"   Maturity Amount (A)  : Rs. {maturity_compound_value:.2f}")
    print("=" * 52)


def passbook_view(accounts_db):
    """
    Screen 11: Views the complete passbook ledger of an account.
    """
    print("\n--- VIEW ACCOUNT PASSBOOK ---")
    acc_str = input("Enter Account Number: ").strip()
    if not is_only_digits(acc_str):
        print("Error: Account number must be numeric.")
        return

    account_no = int(acc_str)
    if account_no not in accounts_db:
        print(f"Error: Account #{account_no} was not found.")
        return

    accounts_db[account_no].display_passbook()


# ============================================================================
# MAIN APPLICATION LOOP
# ============================================================================

def main():
    """
    Main application orchestrator.
    Demonstrates:
    - while loop
    - if-elif-else statements
    - break and continue statements
    """
    # Initialize in-memory database with realistic seed accounts
    accounts_db, registered_mobiles = setup_initial_bank_data()

    print("\n=======================================================")
    print("     NAMASTE! WELCOME TO INDIAN BANKING SYSTEM")
    print("  Course: Python Essentials (First-Year Student Project)")
    print("=======================================================")

    while True:
        print("\n=======================================================")
        print("                     MAIN MENU")
        print("=======================================================")
        print("  1. Open New Bank Account")
        print("  2. View Account Details")
        print("  3. Deposit Funds")
        print("  4. Withdraw Cash")
        print("  5. Check Account Balance")
        print("  6. Transfer Money Between Accounts")
        print("  7. Display All Registered Accounts")
        print("  8. Search for an Account")
        print("  9. Update Customer Profile / Services")
        print(" 10. Calculate Interest (Simple & Compound)")
        print(" 11. View Passbook Statement")
        print(" 12. Exit Application")
        print("=======================================================")

        choice = input("Enter your choice (1-12): ").strip()

        # Navigation routing using if-elif-else
        if choice == "1":
            open_account_view(accounts_db, registered_mobiles)
        elif choice == "2":
            view_account_view(accounts_db)
        elif choice == "3":
            deposit_view(accounts_db)
        elif choice == "4":
            withdraw_view(accounts_db)
        elif choice == "5":
            check_balance_view(accounts_db)
        elif choice == "6":
            transfer_view(accounts_db)
        elif choice == "7":
            display_all_accounts_view(accounts_db)
        elif choice == "8":
            search_account_view(accounts_db)
        elif choice == "9":
            update_info_view(accounts_db, registered_mobiles)
        elif choice == "10":
            interest_view(accounts_db)
        elif choice == "11":
            passbook_view(accounts_db)
        elif choice == "12":
            print("\n=======================================================")
            print("  Thank you for banking with us.")
            print("  Namaste! Have a wonderful day ahead.")
            print("=======================================================\n")
            # break terminates the while True loop cleanly
            break
        else:
            print("Invalid selection! Please enter a number between 1 and 12.")


# Standard Python file entry point check
if __name__ == "__main__":
    main()
