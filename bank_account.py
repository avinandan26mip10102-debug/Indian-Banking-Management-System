"""
bank_account.py - BankAccount Class and Account State Management
Course: Python Essentials (First-Year Student Academic Project)

Student Explanation:
In this module, I am implementing Object-Oriented Programming (OOP).
I created the BankAccount class which encapsulates all properties of a customer's account:
- Identification (number, name, age, phone, branch, category)
- Financial balance (float)
- Digital banking permissions (bitwise flags)
- Transaction ledger (a list of immutable tuples)
- High-efficiency numeric array storing recent transaction amounts ('d' double)
I also include a setup function that initializes realistic seed accounts for quick testing.
"""

from array import array

from constants import (
    ALLOWED_ACCOUNT_TYPES,
    MIN_BALANCE_SAVINGS,
    MIN_BALANCE_CURRENT,
    SERVICE_FLAG_NET_BANKING,
    SERVICE_FLAG_ATM_CARD,
    SERVICE_FLAG_SMS_ALERTS,
    SERVICE_FLAG_CHEQUE_BOOK,
    DEFAULT_ENABLED_SERVICES
)
from security_tools import (
    check_service_permission,
    toggle_service_permission,
    create_security_token,
    generate_audit_checksum
)


class BankAccount:
    """
    Represents an Indian bank account.
    Demonstrates:
    - Object-Oriented Programming (attributes, methods, encapsulation)
    - type() function usage to inspect variable types
    - Identity operators: 'is' and 'is not'
    - Array data structure: storing floating-point amounts efficiently ('d' double)
    - Tuples: immutable passbook records (txn_id, description, amount, balance_after)
    """

    def __init__(self, account_number, customer_name, age, mobile_number,
                 account_type, initial_deposit, branch_code="SBIN001"):
        # Explicit type conversion and attribute assignment
        self.account_number = int(account_number)
        self.customer_name = str(customer_name)
        self.age = int(age)
        self.mobile_number = str(mobile_number)
        self.account_type = str(account_type)
        self.balance = float(initial_deposit)
        self.branch_code = str(branch_code)

        # Bitwise flags representing active digital services (ATM Card & SMS Alerts on by default)
        self.service_flags = DEFAULT_ENABLED_SERVICES

        # Passbook ledger: List of tuples -> (txn_id, description, amount, balance_after)
        self.passbook = []

        # Standard library array storing numeric transaction amounts in memory
        # Typecode 'd' represents double-precision floating-point numbers
        self.recent_amounts_array = array('d', [float(initial_deposit)])

        # Record initial opening deposit
        initial_entry = (1, "Account Opening Deposit", float(initial_deposit), self.balance)
        self.passbook.append(initial_entry)

    def deposit(self, amount):
        """
        Deposits money into the account.
        Demonstrates:
        - Relational operator (<=)
        - Assignment operator (+=)
        - Creating an immutable tuple
        - Appending to list and array
        """
        if amount <= 0:
            print("Deposit Error: Deposit amount must be greater than zero.")
            return False

        # Add amount using addition assignment operator
        self.balance += amount

        # Create an immutable tuple for passbook record
        txn_id = len(self.passbook) + 1
        txn_record = (txn_id, "Cash Deposit", float(amount), self.balance)
        self.passbook.append(txn_record)

        # Append to our numeric array
        self.recent_amounts_array.append(float(amount))

        print(f"Success: Rs. {amount:.2f} credited successfully.")
        print(f"Updated Available Balance: Rs. {self.balance:.2f}")
        return True

    def withdraw(self, amount):
        """
        Withdraws money from the account adhering to minimum balance and ATM rules.
        Demonstrates:
        - Relational operators (<, <=)
        - Modulus operator (%): Indian ATMs only dispense multiples of Rs. 100
        - Subtraction assignment operator (-=)
        """
        if amount <= 0:
            print("Withdrawal Error: Amount must be greater than zero.")
            return False

        # Modulus check: Indian ATM currency constraint (multiples of 100)
        if int(amount) % 100 != 0:
            print("Withdrawal Error: Cash withdrawal must be in multiples of Rs. 100.")
            return False

        # Determine minimum balance threshold based on account type
        if self.account_type == "Savings":
            min_required = MIN_BALANCE_SAVINGS
        else:
            min_required = MIN_BALANCE_CURRENT

        # Check if the requested withdrawal leaves balance below minimum requirement
        if (self.balance - amount) < min_required:
            print("Withdrawal Error: Insufficient funds!")
            print(f"A mandatory minimum balance of Rs. {min_required:.2f} is required for {self.account_type} accounts.")
            available_limit = self.balance - min_required
            if available_limit < 0:
                available_limit = 0.0
            print(f"Current Balance: Rs. {self.balance:.2f} | Max Withdrawable: Rs. {available_limit:.2f}")
            return False

        # Subtraction assignment operator
        self.balance -= amount

        # Log to passbook as an immutable tuple
        txn_id = len(self.passbook) + 1
        txn_record = (txn_id, "Cash Withdrawal", float(amount), self.balance)
        self.passbook.append(txn_record)

        # Track amount in numeric array
        self.recent_amounts_array.append(float(amount))

        print(f"Success: Rs. {amount:.2f} debited successfully.")
        print(f"Remaining Available Balance: Rs. {self.balance:.2f}")
        return True

    def check_balance(self):
        """Returns the current balance."""
        return self.balance

    def transfer_to(self, target_account, amount):
        """
        Transfers funds from this account to another BankAccount instance.
        Demonstrates:
        - Identity Operator 'is': Ensures source and destination are not the same object!
        - Identity Operator 'is not': Ensures target account object is valid
        - Nested conditions
        """
        # Identity Check: Cannot transfer to self
        if self is target_account:
            print("Transfer Error: Source and destination accounts cannot be the exact same account!")
            return False

        if target_account is None:
            print("Transfer Error: Destination account does not exist.")
            return False

        if amount <= 0:
            print("Transfer Error: Transfer amount must be positive.")
            return False

        # Check sender's minimum balance
        if self.account_type == "Savings":
            min_required = MIN_BALANCE_SAVINGS
        else:
            min_required = MIN_BALANCE_CURRENT

        if (self.balance - amount) < min_required:
            print(f"Transfer Error: Insufficient balance to maintain required minimum balance of Rs. {min_required:.2f}.")
            return False

        # Deduct from sender
        self.balance -= amount
        sender_entry = (
            len(self.passbook) + 1,
            f"Transfer to Acc #{target_account.account_number}",
            float(amount),
            self.balance
        )
        self.passbook.append(sender_entry)
        self.recent_amounts_array.append(float(amount))

        # Credit to receiver
        target_account.balance += amount
        receiver_entry = (
            len(target_account.passbook) + 1,
            f"Transfer from Acc #{self.account_number}",
            float(amount),
            target_account.balance
        )
        target_account.passbook.append(receiver_entry)
        target_account.recent_amounts_array.append(float(amount))

        print(f"Success: Rs. {amount:.2f} transferred successfully to Account #{target_account.account_number} ({target_account.customer_name}).")
        print(f"Your Updated Balance: Rs. {self.balance:.2f}")
        return True

    def display_details(self):
        """
        Displays complete profile details of the account.
        Demonstrates:
        - type() function to display data types as required by syllabus
        - Bitwise checking of banking services
        - Generating checksum authentication token
        """
        print("\n" + "=" * 52)
        print(f"        CUSTOMER ACCOUNT PROFILE: #{self.account_number}")
        print("=" * 52)
        print(f"Account Holder Name : {self.customer_name}")
        print(f"Customer Age        : {self.age} years")
        print(f"Registered Mobile   : {self.mobile_number}")
        print(f"Account Category    : {self.account_type} Account")
        print(f"Branch IFSC Code    : {self.branch_code}")
        print(f"Available Balance   : Rs. {self.balance:.2f}")

        # Demonstrating type() function as required by syllabus
        print("-" * 52)
        print(f"Data Type of Acc No : {type(self.account_number).__name__}")
        print(f"Data Type of Balance: {type(self.balance).__name__}")

        # Bitwise service inspection
        print("-" * 52)
        print("Active Digital Banking Services (Bitwise Checked):")
        net_status = "Enabled" if check_service_permission(self.service_flags, SERVICE_FLAG_NET_BANKING) else "Disabled"
        atm_status = "Enabled" if check_service_permission(self.service_flags, SERVICE_FLAG_ATM_CARD) else "Disabled"
        sms_status = "Enabled" if check_service_permission(self.service_flags, SERVICE_FLAG_SMS_ALERTS) else "Disabled"
        chq_status = "Enabled" if check_service_permission(self.service_flags, SERVICE_FLAG_CHEQUE_BOOK) else "Disabled"
        print(f" - Internet Banking : {net_status}")
        print(f" - ATM / Debit Card : {atm_status}")
        print(f" - SMS Alerts       : {sms_status}")
        print(f" - Cheque Book      : {chq_status}")

        # Bitwise security token inspection
        token_val = create_security_token(self.account_number)
        shift_chk, invert_chk = generate_audit_checksum(self.service_flags)
        print(f"Security Token (<<, &): {token_val}")
        print(f"Audit Flag Shift (>>) : {shift_chk} | Inverted (~): {invert_chk}")
        print("=" * 52)

    def display_passbook(self):
        """
        Prints the complete passbook ledger.
        Demonstrates:
        - for loop iterating over list of tuples
        - Tuple unpacking: txn_id, desc, amt, bal = entry
        - Inspecting array values
        """
        print("\n" + "=" * 65)
        print(f"             PASSBOOK STATEMENT: ACCOUNT #{self.account_number}")
        print("=" * 65)
        print(f"{'Txn #':<8}{'Transaction Details':<28}{'Amount (Rs.)':<15}{'Balance (Rs.)':<12}")
        print("-" * 65)

        for entry in self.passbook:
            txn_id, desc, amt, bal = entry
            print(f"{txn_id:<8}{desc:<28}{amt:<15.2f}{bal:<12.2f}")

        print("-" * 65)
        print(f"Total Transactions Logged: {len(self.passbook)}")
        
        # Displaying array elements
        print("Recent Amounts Array (Numeric memory dump):")
        formatted_array_items = []
        for val in self.recent_amounts_array:
            formatted_array_items.append(f"{val:.2f}")
        print(" [ " + ", ".join(formatted_array_items) + " ]")
        print("=" * 65)

    def update_name(self, new_name):
        """Updates the customer's legal name."""
        self.customer_name = str(new_name)

    def update_phone(self, new_phone):
        """Updates the customer's registered phone number."""
        self.mobile_number = str(new_phone)

    def toggle_service(self, service_mask):
        """
        Toggles a banking service flag using bitwise XOR (^).
        """
        self.service_flags = toggle_service_permission(self.service_flags, service_mask)


def setup_initial_bank_data():
    """
    Sets up initial pre-loaded accounts in memory so the student or evaluator
    can immediately test deposits, withdrawals, transfers, and balance checks
    without having to manually create accounts every time the program restarts.
    Returns:
    - accounts_db: Dictionary mapping account_number (int) -> BankAccount object
    - registered_mobiles: Set storing unique 10-digit mobile numbers
    """
    accounts_db = {}
    registered_mobiles = set()

    # Seed Account 1: Aarav Sharma (Savings Account)
    acc1 = BankAccount(
        account_number=1001,
        customer_name="Aarav Sharma",
        age=28,
        mobile_number="9876543210",
        account_type="Savings",
        initial_deposit=15000.0,
        branch_code="SBIN001"
    )
    # Enable Internet Banking for Aarav
    acc1.service_flags = acc1.service_flags | SERVICE_FLAG_NET_BANKING

    # Seed Account 2: Priya Patel (Current Account)
    acc2 = BankAccount(
        account_number=1002,
        customer_name="Priya Patel",
        age=34,
        mobile_number="9123456780",
        account_type="Current",
        initial_deposit=25000.0,
        branch_code="HDFC002"
    )

    # Seed Account 3: Rohan Verma (Savings Account)
    acc3 = BankAccount(
        account_number=1003,
        customer_name="Rohan Verma",
        age=22,
        mobile_number="9988776655",
        account_type="Savings",
        initial_deposit=8000.0,
        branch_code="ICIC003"
    )

    # Add to dictionary (key = account number, value = BankAccount instance)
    accounts_db[acc1.account_number] = acc1
    accounts_db[acc2.account_number] = acc2
    accounts_db[acc3.account_number] = acc3

    # Add to set (ensures mobile numbers are unique)
    registered_mobiles.add(acc1.mobile_number)
    registered_mobiles.add(acc2.mobile_number)
    registered_mobiles.add(acc3.mobile_number)

    return accounts_db, registered_mobiles
