"""
security_tools.py - Bitwise Security Operations and Service Flags
Course: Python Essentials (First-Year Student Academic Project)

Student Explanation:
In our Python course, we studied bitwise operators (&, |, ^, ~, <<, >>).
In this file, I am applying them to manage digital banking permissions
(Net Banking, ATM Card, SMS Alerts, Cheque Book) and compute security tokens.
Working with bits directly is efficient and demonstrates binary manipulation!
"""


def check_service_permission(service_flags, service_mask):
    """
    Checks if a specific service bit is active using Bitwise AND (&).
    If the bit at service_mask is 1, the result is non-zero (True).
    """
    masked_result = service_flags & service_mask
    return masked_result != 0


def grant_service_permission(service_flags, service_mask):
    """
    Enables a specific banking service using Bitwise OR (|).
    Bitwise OR turns on the requested bit without modifying other bits.
    """
    updated_flags = service_flags | service_mask
    return updated_flags


def toggle_service_permission(service_flags, service_mask):
    """
    Flips a banking service ON or OFF using Bitwise XOR (^).
    If the service was 1, XOR turns it to 0.
    If the service was 0, XOR turns it to 1.
    """
    toggled_flags = service_flags ^ service_mask
    return toggled_flags


def create_security_token(account_num):
    """
    Generates a sample 8-bit security checksum token for account authentication.
    Demonstrates:
    - Bitwise Left Shift (<<): Shifts bits left by 2 positions (multiplies by 4)
    - Bitwise AND (&): Masks with 255 (0xFF) to keep the token within 8 bits (0-255)
    """
    shifted_val = account_num << 2
    token_byte = shifted_val & 255
    return token_byte


def generate_audit_checksum(service_flags):
    """
    Demonstrates Bitwise Right Shift (>>) and Bitwise NOT (~).
    Used during periodic banking security audits to verify flag integrity.
    """
    # Bitwise Right Shift: shifts bits right by 1 position (integer division by 2)
    shifted_flags = service_flags >> 1
    
    # Bitwise NOT: inverts all bits (~x = -(x + 1) in Python's two's complement)
    inverted_flags = ~service_flags
    
    return shifted_flags, inverted_flags
