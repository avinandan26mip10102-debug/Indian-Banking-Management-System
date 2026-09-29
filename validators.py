"""
validators.py - User Input Validation Using Fundamental Python Concepts
Course: Python Essentials (First-Year Student Academic Project)

Student Explanation:
Since our syllabus has not covered regex or try-except blocks yet,
I am implementing pure algorithmic validation routines using for loops,
if-elif-else branches, relational operators, and membership operators ('in' / 'not in').
"""

from constants import VALID_BRANCH_CODES, ALLOWED_ACCOUNT_TYPES


def is_only_digits(user_input):
    """
    Checks if a string consists entirely of digits (0-9).
    Demonstrates:
    - len() function to reject empty strings
    - for loop traversing each character
    - Membership operator 'not in'
    """
    if len(user_input) == 0:
        return False
        
    for character in user_input:
        if character not in "0123456789":
            return False
            
    return True


def is_valid_rupee_amount(user_input):
    """
    Checks if an input string is a valid positive floating-point amount.
    Accepts whole numbers ('1500') or valid decimals ('250.75').
    Rejects negatives, letters, and multiple dots ('12.34.56').
    Demonstrates:
    - for loop and counter variable
    - if-elif-else logic
    - Membership operators
    """
    if len(user_input) == 0 or user_input == ".":
        return False

    decimal_dot_count = 0
    for char in user_input:
        if char == ".":
            decimal_dot_count += 1
            # A valid decimal number cannot have more than one dot
            if decimal_dot_count > 1:
                return False
        elif char not in "0123456789":
            return False

    return True


def is_valid_indian_phone(phone_str):
    """
    Validates a 10-digit Indian mobile number.
    According to the Indian Telecom Regulatory Authority (TRAI),
    mobile numbers have 10 digits and must start with 6, 7, 8, or 9.
    Demonstrates:
    - len() checking exactly 10 digits
    - Logical AND operator (and)
    - Membership operator ('in') with a tuple of allowed first digits
    """
    if len(phone_str) == 10 and is_only_digits(phone_str):
        first_digit = phone_str[0]
        if first_digit in ("6", "7", "8", "9"):
            return True
            
    return False


def is_valid_applicant_age(age_val):
    """
    Checks if customer age is within valid limits for opening an individual bank account.
    In Indian banks, a customer opening a standard independent account must be an adult (18+).
    Demonstrates:
    - Relational operators (>=, <=)
    - Logical AND operator (and)
    """
    if age_val >= 18 and age_val <= 100:
        return True
    else:
        return False


def is_valid_ifsc_branch(branch_str):
    """
    Verifies that the entered branch code exists in our frozen set.
    Demonstrates:
    - Membership operator 'in' with a frozenset
    """
    return branch_str in VALID_BRANCH_CODES
