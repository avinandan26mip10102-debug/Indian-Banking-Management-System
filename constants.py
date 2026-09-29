"""
constants.py - System Constants and Banking Configurations
Course: Python Essentials (First-Year Student Academic Project)

Student Explanation:
In this module, I am defining fixed configurations for our bank.
Putting fixed values in one place prevents typos and keeps the project organized.
I am using tuples and frozensets because both are immutable data structures,
meaning their values cannot be changed while the program is running.
"""

# ============================================================================
# 1. IMMUTABLE TUPLE: Allowed Account Types
# ============================================================================
# A tuple is used here because bank account categories are fixed in our system.
ALLOWED_ACCOUNT_TYPES = ("Savings", "Current")

# Minimum balance thresholds in Indian Rupees (INR)
# In Indian banks, Savings accounts require a smaller minimum balance than Current accounts.
MIN_BALANCE_SAVINGS = 500.0
MIN_BALANCE_CURRENT = 1000.0

# ============================================================================
# 2. IMMUTABLE FROZENSET: Authorized Indian Bank Branch Codes
# ============================================================================
# A frozenset is an immutable set. Once created, elements cannot be added or removed.
# We use sample Indian IFSC-like branch codes here.
VALID_BRANCH_CODES = frozenset({"SBIN001", "HDFC002", "ICIC003", "PNB0004"})

# ============================================================================
# 3. BITWISE PERMISSION FLAGS (Powers of 2 for Binary Bit Operations)
# ============================================================================
# Instead of storing multiple boolean variables for banking services,
# we use single-bit flags (powers of 2) as taught in our Python operator classes.
#   Bit 0 (value 1) -> Net Banking
#   Bit 1 (value 2) -> ATM Debit Card
#   Bit 2 (value 4) -> SMS Alerts
#   Bit 3 (value 8) -> Cheque Book
SERVICE_FLAG_NET_BANKING = 1   # Binary: 0001 (1 << 0)
SERVICE_FLAG_ATM_CARD    = 2   # Binary: 0010 (1 << 1)
SERVICE_FLAG_SMS_ALERTS  = 4   # Binary: 0100 (1 << 2)
SERVICE_FLAG_CHEQUE_BOOK = 8   # Binary: 1000 (1 << 3)

# Default services activated during account opening (ATM Card + SMS Alerts)
# Bitwise OR combines the flags: 2 | 4 = 6 (Binary 0110)
DEFAULT_ENABLED_SERVICES = SERVICE_FLAG_ATM_CARD | SERVICE_FLAG_SMS_ALERTS
