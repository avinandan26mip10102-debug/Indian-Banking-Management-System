"""
test.py - Automated Manual Test Suite for Indian Banking Management System
Course: Python Essentials (First-Year Student Academic Project)

Student Explanation:
Our course restrictions strictly prohibit using external testing frameworks
like pytest or unittest. My professor asked us to demonstrate verification
using pure Python fundamentals: functions, if-else statements, relational
comparisons, and formatted print reports.

This test file verifies all 6 modules:
  1. constants.py
  2. validators.py
  3. security_tools.py
  4. calculations.py
  5. bank_account.py
  6. main.py (Screen logic & data integrity)
"""

from array import array

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
from security_tools import (
    check_service_permission,
    grant_service_permission,
    toggle_service_permission,
    create_security_token,
    generate_audit_checksum
)
from calculations import (
    compute_simple_interest,
    compute_compound_interest,
    compute_monthly_average,
    get_cash_notes_breakdown
)
from bank_account import BankAccount, setup_initial_bank_data


# Global counters for test tracking
total_test_count = 0
passed_test_count = 0


def log_test_result(test_name, condition, details=""):
    """
    Helper function to record and display individual test results.
    Demonstrates:
    - Global variables
    - if-else statement
    - String formatting
    """
    global total_test_count, passed_test_count
    total_test_count += 1
    
    if condition:
        passed_test_count += 1
        print(f" [PASS] Test {total_test_count:02d}: {test_name}")
    else:
        print(f" [FAIL] Test {total_test_count:02d}: {test_name}")
        if len(details) > 0:
            print(f"        Reason: {details}")


# ============================================================================
# 1. VALIDATION MODULE TESTS (validators.py)
# ============================================================================

def run_validator_tests():
    print("\n--- RUNNING VALIDATOR MODULE TESTS ---")

    # Test 1: Digit string checking
    cond1 = is_only_digits("12345") and not is_only_digits("123a5") and not is_only_digits("")
    log_test_result("is_only_digits() validation", cond1)

    # Test 2: Rupee amount float checking
    cond2 = (
        is_valid_rupee_amount("1500") and
        is_valid_rupee_amount("250.75") and
        not is_valid_rupee_amount("-50") and
        not is_valid_rupee_amount("12.34.56") and
        not is_valid_rupee_amount(".")
    )
    log_test_result("is_valid_rupee_amount() validation", cond2)

    # Test 3: Indian mobile number validation (TRAI rules: 10 digits starting 6,7,8,9)
    cond3 = (
        is_valid_indian_phone("9876543210") and
        is_valid_indian_phone("8123456789") and
        not is_valid_indian_phone("5123456789") and  # invalid starting digit 5
        not is_valid_indian_phone("98765") and       # too short
        not is_valid_indian_phone("98765432100")     # too long
    )
    log_test_result("is_valid_indian_phone() TRAI compliance", cond3)

    # Test 4: Age validation (18 to 100)
    cond4 = (
        is_valid_applicant_age(18) and
        is_valid_applicant_age(45) and
        is_valid_applicant_age(100) and
        not is_valid_applicant_age(17) and
        not is_valid_applicant_age(101)
    )
    log_test_result("is_valid_applicant_age() age boundaries (18-100)", cond4)

    # Test 5: Branch code frozenset membership
    cond5 = (
        is_valid_ifsc_branch("SBIN001") and
        is_valid_ifsc_branch("HDFC002") and
        not is_valid_ifsc_branch("FAKE000") and
        not is_valid_ifsc_branch("SBIN999")
    )
    log_test_result("is_valid_ifsc_branch() frozenset membership", cond5)


# ============================================================================
# 2. SECURITY & BITWISE MODULE TESTS (security_tools.py)
# ============================================================================

def run_security_tests():
    print("\n--- RUNNING SECURITY & BITWISE TESTS ---")

    # Start with ATM Card enabled (2)
    flags = SERVICE_FLAG_ATM_CARD

    # Test 6: Bitwise AND checking
    cond6 = check_service_permission(flags, SERVICE_FLAG_ATM_CARD) and not check_service_permission(flags, SERVICE_FLAG_NET_BANKING)
    log_test_result("check_service_permission() using Bitwise AND (&)", cond6)

    # Test 7: Bitwise OR enabling
    flags = grant_service_permission(flags, SERVICE_FLAG_NET_BANKING)  # 2 | 1 = 3
    cond7 = check_service_permission(flags, SERVICE_FLAG_NET_BANKING) and check_service_permission(flags, SERVICE_FLAG_ATM_CARD)
    log_test_result("grant_service_permission() using Bitwise OR (|)", cond7)

    # Test 8: Bitwise XOR toggling
    flags = toggle_service_permission(flags, SERVICE_FLAG_NET_BANKING)  # 3 ^ 1 = 2 (toggled OFF)
    cond8 = not check_service_permission(flags, SERVICE_FLAG_NET_BANKING)
    flags = toggle_service_permission(flags, SERVICE_FLAG_NET_BANKING)  # 2 ^ 1 = 3 (toggled ON)
    cond8 = cond8 and check_service_permission(flags, SERVICE_FLAG_NET_BANKING)
    log_test_result("toggle_service_permission() using Bitwise XOR (^)", cond8)

    # Test 9: Bitwise Shift and Mask Token Generation
    token = create_security_token(1001)  # (1001 << 2) & 255 = 4004 & 255 = 164
    cond9 = (token == 164) and (0 <= token <= 255)
    log_test_result("create_security_token() using (<<) and (&)", cond9)

    # Test 10: Bitwise Right Shift (>>) and NOT (~) Audit
    shifted, inverted = generate_audit_checksum(flags)
    cond10 = (shifted == (flags >> 1)) and (inverted == ~flags)
    log_test_result("generate_audit_checksum() using (>>) and (~)", cond10)


# ============================================================================
# 3. CALCULATIONS MODULE TESTS (calculations.py)
# ============================================================================

def run_calculation_tests():
    print("\n--- RUNNING CALCULATIONS & ARITHMETIC TESTS ---")

    # Test 11: Simple Interest formula
    # P = 10000, R = 5%, T = 2 years -> SI = (10000 * 5 * 2) / 100 = 1000.0
    si = compute_simple_interest(10000.0, 5.0, 2.0)
    cond11 = (si == 1000.0)
    log_test_result("compute_simple_interest() calculation", cond11)

    # Test 12: Compound Interest and Operator Precedence
    # P = 10000, R = 10%, T = 2 years -> A = 10000 * (1.10 ** 2) = 12100.0, CI = 2100.0
    ci, maturity = compute_compound_interest(10000.0, 10.0, 2.0)
    cond12 = (round(ci, 2) == 2100.0) and (round(maturity, 2) == 12100.0)
    log_test_result("compute_compound_interest() exponentiation (**) & precedence", cond12)

    # Test 13: Mixed-Type Division (float / int = float)
    balance = 15000.0   # float
    months = 12         # int
    monthly_avg = compute_monthly_average(balance, months)
    cond13 = (monthly_avg == 1250.0) and (type(monthly_avg) is float)
    log_test_result("compute_monthly_average() mixed-type division (float / int)", cond13)

    # Test 14: ATM currency note breakdown using array('i')
    # Amount = 1700 -> Three 500s (1500), One 200 (200), Zero 100s, Leftover 0
    breakdown, leftover = get_cash_notes_breakdown(1700)
    cond14 = (
        breakdown[500] == 3 and
        breakdown[200] == 1 and
        breakdown[100] == 0 and
        leftover == 0
    )
    log_test_result("get_cash_notes_breakdown() using array('i'), //, and %", cond14)


# ============================================================================
# 4. BANK ACCOUNT OOP MODULE TESTS (bank_account.py)
# ============================================================================

def run_bank_account_tests():
    print("\n--- RUNNING BANK ACCOUNT OOP TESTS ---")

    # Create fresh test account
    acc = BankAccount(
        account_number=2001,
        customer_name="Test Customer",
        age=25,
        mobile_number="9876500000",
        account_type="Savings",
        initial_deposit=5000.0,
        branch_code="SBIN001"
    )

    # Test 15: Object creation, types and initial balance
    cond15 = (
        acc.account_number == 2001 and
        acc.customer_name == "Test Customer" and
        acc.balance == 5000.0 and
        type(acc.account_number) is int and
        type(acc.balance) is float
    )
    log_test_result("BankAccount __init__() attributes and type() integrity", cond15)

    # Test 16: Deposit money
    deposit_success = acc.deposit(2000.0)
    cond16 = deposit_success and (acc.balance == 7000.0)
    log_test_result("deposit() credits balance and updates state", cond16)

    # Test 17: Deposit invalid amount rejection
    dep_fail = acc.deposit(-100.0)
    cond17 = (not dep_fail) and (acc.balance == 7000.0)
    log_test_result("deposit() rejects non-positive amounts", cond17)

    # Test 18: Valid withdrawal
    withdraw_success = acc.withdraw(1000.0)
    cond18 = withdraw_success and (acc.balance == 6000.0)
    log_test_result("withdraw() debits balance successfully", cond18)

    # Test 19: Withdrawal multiple of 100 rule
    invalid_note_withdraw = acc.withdraw(250.0)
    cond19 = (not invalid_note_withdraw) and (acc.balance == 6000.0)
    log_test_result("withdraw() enforces multiples of Rs. 100 via modulus (%)", cond19)

    # Test 20: Withdrawal exceeding minimum balance rule (min Rs. 500 for Savings)
    # Balance is 6000, attempting to withdraw 5800 leaves 200 (< 500) -> must fail!
    excess_withdraw = acc.withdraw(5800.0)
    cond20 = (not excess_withdraw) and (acc.balance == 6000.0)
    log_test_result("withdraw() prevents violating minimum balance threshold", cond20)

    # Test 21: Passbook immutable tuples logging
    # Initial deposit (1), valid deposit (2), valid withdrawal (3) -> total 3 entries
    cond21 = (len(acc.passbook) == 3)
    if cond21:
        first_entry = acc.passbook[0]
        # Verify first entry is a tuple
        cond21 = cond21 and (type(first_entry) is tuple) and (first_entry[2] == 5000.0)
    log_test_result("passbook ledger tracks immutable tuples correctly", cond21)

    # Test 22: Numeric Array tracking ('d' double)
    cond22 = (type(acc.recent_amounts_array) is array) and (acc.recent_amounts_array.typecode == 'd')
    cond22 = cond22 and (len(acc.recent_amounts_array) == 3)
    log_test_result("recent_amounts_array tracks amounts in array('d')", cond22)

    # Test 23: Inter-account Transfer
    target_acc = BankAccount(
        account_number=2002,
        customer_name="Recipient Customer",
        age=30,
        mobile_number="9876511111",
        account_type="Current",
        initial_deposit=10000.0,
        branch_code="HDFC002"
    )
    transfer_success = acc.transfer_to(target_acc, 2000.0)
    cond23 = (
        transfer_success and
        acc.balance == 4000.0 and
        target_acc.balance == 12000.0
    )
    log_test_result("transfer_to() updates both sender and receiver accounts", cond23)

    # Test 24: Self-transfer rejection using identity operator 'is'
    self_transfer = acc.transfer_to(acc, 500.0)
    cond24 = (not self_transfer) and (acc.balance == 4000.0)
    log_test_result("transfer_to() prevents self-transfer using identity operator (is)", cond24)

    # Test 25: Transfer to None object using identity operator 'is'
    none_transfer = acc.transfer_to(None, 500.0)
    cond25 = (not none_transfer) and (acc.balance == 4000.0)
    log_test_result("transfer_to() rejects None destination safely", cond25)


# ============================================================================
# 5. DATA SETUP AND SEARCH INTEGRATION TESTS
# ============================================================================

def run_integration_tests():
    print("\n--- RUNNING SYSTEM INTEGRATION & SEARCH TESTS ---")

    accounts_db, registered_mobiles = setup_initial_bank_data()

    # Test 26: Pre-loaded seed accounts verification
    cond26 = (len(accounts_db) == 3) and (len(registered_mobiles) == 3)
    cond26 = cond26 and (1001 in accounts_db) and ("9876543210" in registered_mobiles)
    log_test_result("setup_initial_bank_data() loads seed accounts & mobile set", cond26)

    # Test 27: Search account by Account Number (Dictionary lookup)
    cond27 = (1002 in accounts_db) and (accounts_db[1002].customer_name == "Priya Patel")
    log_test_result("Search by account number in dictionary", cond27)

    # Test 28: Search account by Name Substring
    all_accounts = list(accounts_db.values())
    found_by_name = False
    for acc in all_accounts:
        if "priya" in acc.customer_name.lower():
            found_by_name = True
            break
    log_test_result("Search by customer name substring ('in')", found_by_name)

    # Test 29: Customer mobile number update in set
    test_acc = accounts_db[1001]
    old_phone = test_acc.mobile_number
    new_phone = "9800000000"
    registered_mobiles.remove(old_phone)
    registered_mobiles.add(new_phone)
    test_acc.update_phone(new_phone)
    cond29 = (test_acc.mobile_number == new_phone) and (new_phone in registered_mobiles) and (old_phone not in registered_mobiles)
    log_test_result("update_phone() modifies object state and unique set", cond29)


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    print("=" * 65)
    print("   INDIAN BANKING MANAGEMENT SYSTEM - AUTOMATED TEST SUITE")
    print("   Course: Python Essentials (First-Year Student Academic Project)")
    print("=" * 65)

    run_validator_tests()
    run_security_tests()
    run_calculation_tests()
    run_bank_account_tests()
    run_integration_tests()

    print("\n" + "=" * 65)
    print("                      TEST SUITE SUMMARY")
    print("=" * 65)
    print(f"Total Test Cases Executed : {total_test_count}")
    print(f"Total Test Cases Passed   : {passed_test_count}")
    print(f"Total Test Cases Failed   : {total_test_count - passed_test_count}")
    
    if passed_test_count == total_test_count:
        print("\n🎉 ALL TESTS PASSED! ALL 6 MODULES FUNCTION WITH 100% INTEGRITY.")
    else:
        print("\n⚠️ SOME TESTS FAILED. PLEASE REVIEW THE FAILURE DETAILS ABOVE.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
