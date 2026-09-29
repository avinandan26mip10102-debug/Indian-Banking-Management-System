"""
calculations.py - Banking Mathematics and Operator Demonstrations
Course: Python Essentials (First-Year Student Academic Project)

Student Explanation:
This module handles all the financial mathematics for our banking simulation:
1. Simple Interest (SI) using arithmetic multiplication and division
2. Compound Interest (CI) using exponentiation (**) and operator precedence
3. Monthly Average Balance (MAB) demonstrating mixed-type division (float / int = float)
4. Cash notes breakdown using the Python Standard Library array module, floor division (//),
   and modulus (%)
"""

from array import array


def compute_simple_interest(principal, annual_rate, time_in_years):
    """
    Computes Simple Interest using the standard formula:
      SI = (P * R * T) / 100
    Demonstrates:
    - Arithmetic operators: *, /
    - Parentheses to enforce precedence so the product is calculated before dividing
    """
    interest_amount = (principal * annual_rate * time_in_years) / 100.0
    return interest_amount


def compute_compound_interest(principal, annual_rate, time_in_years):
    """
    Computes Compound Interest (CI) for Indian Fixed Deposit (FD) accounts:
      Maturity Amount A = P * ((1 + R / 100) ** T)
      Compound Interest CI = A - P
    Demonstrates:
    - Exponentiation operator (**)
    - Operator Precedence & Associativity:
        1. (annual_rate / 100.0) is evaluated first inside its own parentheses
        2. 1.0 + rate is computed next
        3. Exponentiation (**) has higher precedence than multiplication (*)
        4. The principal is multiplied by the growth factor
        5. Finally, subtraction (-) gives the interest component
    """
    growth_multiplier = 1.0 + (annual_rate / 100.0)
    maturity_total = principal * (growth_multiplier ** time_in_years)
    interest_earned = maturity_total - principal
    return interest_earned, maturity_total


def compute_monthly_average(balance_val, total_months):
    """
    Calculates the Monthly Average Balance (MAB) for the customer.
    Demonstrates:
    - Division involving mixed data types:
      balance_val is of type float (e.g., 15000.50)
      total_months is of type int (e.g., 12)
      In Python, dividing a float by an int always produces a float!
    """
    monthly_avg = balance_val / total_months
    return monthly_avg


def get_cash_notes_breakdown(withdraw_amount):
    """
    Simulates an Indian ATM cash dispenser breakdown into standard ₹500, ₹200, and ₹100 notes.
    Demonstrates:
    - Array Data Structure: Using Python standard library array('i', [...])
      to store signed integer note values
    - Floor Division (//): Calculates the whole number of notes for each denomination
    - Modulus Operator (%): Calculates remaining cash left to be dispensed by smaller notes
    - Dictionary: Stores denomination -> note count
    """
    # Create an array of integers with typecode 'i'
    currency_notes = array('i', [500, 200, 100])
    dispensed_summary = {}
    remaining_cash = int(withdraw_amount)

    for note in currency_notes:
        # Floor division gives exact note count
        count = remaining_cash // note
        dispensed_summary[note] = count
        
        # Modulus operator keeps the leftover amount
        remaining_cash = remaining_cash % note

    return dispensed_summary, remaining_cash
