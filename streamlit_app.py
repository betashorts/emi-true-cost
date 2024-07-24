import streamlit as st
import numpy as np
from scipy.optimize import fsolve
import pandas as pd

# Function to calculate the NPV of the loan cash flows at a given monthly interest rate
def npv_of_loan(monthly_rate, loan_amount, monthly_payment, loan_period_months):
    npv = loan_amount
    for i in range(1, loan_period_months + 12):
        npv -= monthly_payment / ((1 + monthly_rate) ** i)
    return npv

# Function to calculate the total interest paid using the implicit rate
def calculate_total_interest_paid(loan_amount, monthly_payment, monthly_rate, loan_period_months):
    remaining_loan = loan_amount
    total_interest_paid = 0
    details = []

    for month in range(1, loan_period_months + 1):
        interest_paid = remaining_loan * monthly_rate
        principal_paid = monthly_payment - interest_paid
        remaining_loan -= principal_paid
        total_interest_paid += interest_paid

        # Ensure remaining loan is zero at the end of the loan period
        if month == loan_period_months:
            if abs(remaining_loan) < 1:  # If residual is less than 1 unit of currency
                principal_paid += remaining_loan
                remaining_loan = 0

        details.append({
            "Month": month,
            "Remaining Loan": round(remaining_loan, 2),
            "Interest Paid": round(interest_paid, 2),
            "Principal Paid": round(principal_paid, 2)
        })

    return total_interest_paid, details

# Streamlit App
st.set_page_config(page_title="EMI Rate Calculator", page_icon=":moneybag:", layout="wide")

# Title and Introduction
st.title("EMI Implicit Rate Calculator")
st.write("""
Welcome to the EMI Implicit Rate Calculator!

### Purpose of the Site
When you take out a loan, the advertised interest rate might seem straightforward, but the way EMIs (Equated Monthly Installments) are structured means you often end up paying more than this nominal rate. Our tool helps you understand the actual interest rate you're paying and provides a detailed breakdown of your loan payments.

### How It Works
1. **Enter Your Loan Details**: Provide the loan amount, monthly EMI payment, and the loan term in months.
2. **Calculate Implicit Rate**: Our calculator will determine the actual monthly and annual interest rates you are effectively paying.
3. **View Detailed Breakdown**: See a month-by-month breakdown of your payments, including how much goes towards interest and principal.

By using this tool, you can better understand the true cost of your loan and make more informed financial decisions.
""")

# User inputs
st.header("Enter Your Loan Details")
loan_amount = st.number_input("Loan Amount", value=74000, step=1000)
monthly_payment = st.number_input("Monthly Payment", value=6660, step=100)
loan_period_months = st.number_input("Loan Period (Months)", value=12, step=1)

if st.button("Calculate Implicit Rate"):
    # Use fsolve to find the monthly interest rate that makes the NPV equal to zero
    monthly_rate_guess = 0.01  # Initial guess for the monthly interest rate
    monthly_rate_solution = fsolve(npv_of_loan, monthly_rate_guess, args=(loan_amount, monthly_payment, loan_period_months))[0]

    # Convert the monthly interest rate to an annual interest rate
    annual_rate_solution = (1 + monthly_rate_solution) ** 12 - 1

    # Calculate the total interest paid using the implicit monthly rate
    total_interest_paid, details = calculate_total_interest_paid(loan_amount, monthly_payment, monthly_rate_solution, loan_period_months)
    
    # Display results
    st.header("Results")
    st.write(f"**Monthly Interest Rate:** {monthly_rate_solution * 100:.2f}%")
    st.write(f"**Equivalent Annual Interest Rate:** {annual_rate_solution * 100:.2f}%")
    st.write(f"**Total Interest Paid:** {total_interest_paid:.2f}")

    # Explanation of the table
    st.write("""
    ### Understanding Your EMI Breakdown
    When you take a loan, the interest rate mentioned (e.g., 8% per year) may seem straightforward. However, due to the way EMIs (Equated Monthly Installments) are structured, you actually end up paying interest on the remaining principal each month, which makes the effective interest rate higher than the nominal rate. 

    The table below shows the detailed breakdown of your loan payments:
    - **Month**: The month number of the loan term.
    - **Remaining Loan**: The remaining loan balance at the start of each month.
    - **Interest Paid**: The interest amount paid for that month.
    - **Principal Paid**: The principal amount paid for that month.
    
    By looking at this breakdown, you can see how much of your monthly payment goes towards paying off the interest and how much reduces the principal. This helps you understand the true cost of your loan.
    """)

    # Display detailed table
    st.write("### Payment Details")
    df = pd.DataFrame(details)
    st.dataframe(df)

    # Buy Me a Coffee request
    st.write("### Support This Project")
    st.write("""
    If you found this tool helpful, please consider supporting the project. Your contributions help us maintain and improve this service.
    """)

    # PayPal Buy Me a Coffee button/link
    buy_me_coffee_link = "https://www.paypal.com/ncp/payment/EMZTCUL85J8WE"  # Replace with your PayPal Buy Me a Coffee link
    st.markdown(f"""
    <a href="{buy_me_coffee_link}" target="_blank">
        <img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" alt="Buy Me a Coffee" />
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        .css-1q8dd3e {font-size: 1.2em;}
    </style>
    """, unsafe_allow_html=True)
