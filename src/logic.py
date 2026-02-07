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