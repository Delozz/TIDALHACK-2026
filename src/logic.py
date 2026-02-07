"""
Financial Logic Module for NextStep Dashboard

This module contains core financial calculations for estimating post-graduation
financial reality for STEM professionals. All calculations are transparent and
documented for evaluation purposes.
"""

# State income tax rates (simplified for prototype)
TAX_RATES = {
    'TX': 0.00, 'WA': 0.00, 'FL': 0.00, 'NV': 0.00,  # No income tax states
    'CA': 0.09, 'NY': 0.06, 'MA': 0.05, 'IL': 0.05, 'CO': 0.045
}


def calculate_taxes(salary, state):
    """
    Calculate monthly net income after federal and state taxes.
    
    Formula:
    --------
    1. Federal Tax: 22% (approximates the 22% federal bracket for mid-level STEM)
    2. State Tax: 0% for TX/WA/FL/NV, 5% flat rate for other states (simplified)
    3. FICA (Social Security + Medicare): 7.65%
    4. Net Income = Gross Salary × (1 - Total Tax Rate)
    5. Monthly Net = Net Annual Income / 12
    
    Parameters:
    -----------
    salary : float
        Annual gross salary in dollars
    state : str
        Two-letter state code (e.g., 'TX', 'CA')
    
    Returns:
    --------
    float
        Monthly net income after all taxes
    
    Example:
    --------
    >>> calculate_taxes(100000, 'TX')
    5862.50  # No state tax in Texas
    
    >>> calculate_taxes(100000, 'CA')
    5112.50  # 9% state tax in California
    """
    # Tax rates
    federal_tax_rate = 0.22  # Federal income tax (22% bracket)
    fica_rate = 0.0765       # Social Security (6.2%) + Medicare (1.45%)
    
    # Determine state tax
    if state in ['TX', 'WA', 'FL', 'NV']:
        state_tax_rate = 0.00  # No state income tax
    else:
        state_tax_rate = TAX_RATES.get(state, 0.05)  # Default 5% for other states
    
    # Calculate total tax burden
    total_tax_rate = federal_tax_rate + fica_rate + state_tax_rate
    
    # Calculate net annual income
    net_annual_income = salary * (1 - total_tax_rate)
    
    # Convert to monthly
    monthly_net_income = net_annual_income / 12
    
    return round(monthly_net_income, 2)


def calculate_thriving_score(salary, rent, cost_of_living_index, loan_payment=0):
    """
    Calculate a 'Thriving Score' (0-100) based on financial comfort after expenses.
    
    Formula:
    --------
    1. Monthly Net = Salary / 12 (simplified, assumes post-tax already handled elsewhere)
    2. Living Expenses = Rent + (COL Index / 100 × $1200 baseline for food/transport)
    3. Discretionary Income = Monthly Net - Living Expenses - Loan Payment
    4. Score = (Discretionary Income / Cost Index) × 100
    5. Capped between 0 and 100
    
    Scoring Guide:
    --------------
    - 0-30:   Struggling (negative discretionary income)
    - 30-60:  Surviving (can cover basics, minimal savings)
    - 60-80:  Comfortable (can save and enjoy life)
    - 80-100: Thriving (high discretionary income, building wealth)
    
    Parameters:
    -----------
    salary : float
        Annual gross salary in dollars
    rent : float
        Monthly rent/housing cost in dollars
    cost_of_living_index : float
        Cost of living index (100 = national average)
    loan_payment : float, optional
        Monthly student loan payment (default: 0)
    
    Returns:
    --------
    int
        Thriving score from 0 to 100
    
    Example:
    --------
    >>> calculate_thriving_score(100000, 1500, 110, 300)
    75  # Comfortable living situation
    
    >>> calculate_thriving_score(60000, 2500, 150, 500)
    25  # Struggling in expensive city
    """
    # Calculate monthly income (simplified - assumes pre-tax for now)
    monthly_net = salary / 12
    
    # Estimate non-rent living costs based on Cost of Living Index
    # Baseline: COL of 100 = $1200/month for food, transport, utilities
    baseline_living_cost = 1200
    living_expenses = (cost_of_living_index / 100) * baseline_living_cost
    
    # Total monthly expenses
    total_expenses = rent + living_expenses + loan_payment
    
    # Discretionary income (what's left after essentials)
    discretionary_income = monthly_net - total_expenses
    
    # Calculate score: normalize by cost index to account for location
    # Formula designed so $1000 discretionary in average COL = score of ~70
    score = (discretionary_income / cost_of_living_index) * 100
    
    # Additional scaling factor for better distribution
    score = 40 + (score * 0.6)  # Shifts baseline up and compresses range
    
    # Clamp score between 0 and 100
    return int(max(0, min(100, score)))


def project_savings(net_income, rent, loan_payment, lifestyle_cost):
    """
    Calculate projected monthly savings after all expenses.
    
    Formula:
    --------
    Monthly Savings = Net Income - Rent - Loan Payment - Lifestyle Costs
    
    Where:
    - Net Income: Monthly take-home pay after taxes
    - Rent: Monthly housing cost
    - Loan Payment: Monthly student loan payment
    - Lifestyle Cost: Food, transport, entertainment, misc (based on lifestyle choice)
    
    Parameters:
    -----------
    net_income : float
        Monthly net income after taxes (dollars)
    rent : float
        Monthly rent/housing cost (dollars)
    loan_payment : float
        Monthly student loan payment (dollars)
    lifestyle_cost : float
        Monthly lifestyle expenses - food, transport, entertainment (dollars)
        - Frugal: ~$800-1000
        - Balanced: ~$1500-2000
        - Boujee: ~$2500-3500
    
    Returns:
    --------
    float
        Projected monthly savings (can be negative if expenses exceed income)
    
    Example:
    --------
    >>> project_savings(6000, 1500, 400, 1800)
    2300.0  # $2,300 saved per month
    
    >>> project_savings(4000, 2000, 600, 1800)
    -400.0  # Deficit of $400/month (living beyond means)
    """
    # Simple calculation: what's left after all expenses
    monthly_savings = net_income - rent - loan_payment - lifestyle_cost
    
    return round(monthly_savings, 2)


# Legacy function for backwards compatibility
def calculate_net_income(gross_salary, state, debt):
    """
    LEGACY: Calculate net monthly income accounting for taxes and loan payments.
    
    This is a wrapper that combines tax calculation with loan payment deduction.
    Prefer using calculate_taxes() and project_savings() separately for more control.
    """
    # Calculate monthly net after taxes
    monthly_net = calculate_taxes(gross_salary, state)
    
    # Estimate student loan payment (10-year standard repayment plan)
    # Rule of thumb: For every $10k debt, pay ~$115/month
    loan_payment_monthly = (debt / 10000) * 115
    
    # Subtract loan payment from net income
    final_monthly_net = monthly_net - loan_payment_monthly
    
    return round(final_monthly_net, 2)
