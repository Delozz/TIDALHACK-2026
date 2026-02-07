# File: src/logic.py

def format_currency(amount):
    """Helper to make money look pretty ($1,200)"""
    return f"${int(amount):,}"

def calculate_taxes(gross_salary, state):
    """
    Calculates monthly net income based on simple tax rules.
    """
    # 1. Federal Tax (Flat ~22% estimate for single filers in this bracket)
    fed_tax_rate = 0.22
    
    # 2. State Tax Rules
    no_tax_states = ['TX', 'FL', 'WA', 'NV', 'TN', 'NH', 'SD', 'WY', 'AK']
    
    if state.upper() in no_tax_states:
        state_tax_rate = 0.00
    else:
        state_tax_rate = 0.05  # Flat 5% average for others
        
    total_tax_rate = fed_tax_rate + state_tax_rate
    
    annual_net = gross_salary * (1 - total_tax_rate)
    monthly_net = annual_net / 12
    
    return int(monthly_net)

def calculate_thriving_score(monthly_net, rent, col_index):
    """
    Returns a score 0-100.
    Formula: Uses discretionary income weighted by Cost of Living.
    """
    # Safety check to avoid division by zero
    if col_index == 0: col_index = 50
    
    discretionary = monthly_net - rent
    
    # The Formula requested: (Net - Rent) / COL * 10
    # Example: ($6000 - $2000) / 70 * 10 = 571 (Too high, need to normalize)
    # Adjusted Logic to fit 0-100 scale:
    
    raw_score = (discretionary / col_index) * 1.5
    
    # Cap at 100, Floor at 0
    return int(max(0, min(100, raw_score)))

def project_savings(monthly_net, rent, loan_payment, lifestyle):
    """
    Returns monthly savings after all expenses.
    """
    lifestyle_map = {
        'Frugal': 800,     # Ramen and Netflix
        'Balanced': 1500,  # Gym membership and occasional dinners
        'Boujee': 2500     # Whole Foods and Cocktails
    }
    
    # Default to Balanced if string doesn't match
    lifestyle_cost = lifestyle_map.get(lifestyle, 1500)
    
    savings = monthly_net - rent - loan_payment - lifestyle_cost
    return int(savings)

def project_5yr_wealth(monthly_net, rent, col_index):
    """
    Projects wealth accumulation over 5 years.
    Factors in savings, cost of living, and compound growth.
    
    Args:
        monthly_net: Monthly net income after taxes
        rent: Monthly rent cost
        col_index: Cost of living index (0-100)
        
    Returns:
        int: Projected wealth after 5 years
    """
    # Safety check
    if col_index == 0: 
        col_index = 50
    
    # Calculate discretionary income (after rent)
    discretionary = monthly_net - rent
    
    # Estimate average monthly expenses based on COL
    # Higher COL = higher expenses beyond rent
    col_factor = col_index / 100
    avg_monthly_expenses = 1000 + (col_factor * 1500)  # Base + COL-adjusted expenses
    
    # Monthly savings
    monthly_savings = discretionary - avg_monthly_expenses
    
    # If negative savings, return 0
    if monthly_savings < 0:
        return 0
    
    # Project 5 years with modest investment returns (5% annual = 0.4% monthly approx)
    # Using future value of annuity formula: FV = PMT × [(1 + r)^n - 1] / r
    months = 60  # 5 years
    monthly_rate = 0.004  # ~5% annual return
    
    # Future value calculation
    if monthly_rate > 0:
        wealth = monthly_savings * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        wealth = monthly_savings * months
    
    return int(wealth)
