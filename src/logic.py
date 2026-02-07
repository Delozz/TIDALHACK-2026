TAX_RATES = {
    'TX': 0.00, 'WA': 0.00, 'FL': 0.00, 'NV': 0.00, # No tax states
    'CA': 0.09, 'NY': 0.06, 'MA': 0.05, 'IL': 0.05, 'CO': 0.045
}

def calculate_net_income(gross_salary, state, debt):

    # 1. Taxes
    fed_tax = 0.18
    fica_tax = 0.0765
    state_tax = TAX_RATES.get(state, 0.04) # Default to 4% if unknown
    
    total_tax_rate = fed_tax + fica_tax + state_tax
    net_annual = gross_salary * (1 - total_tax_rate)
    
    # 2. Student Loans (Standard 10-year plan approximation)
    loan_payment_monthly = (debt / 10000) * 115
    
    monthly_net = (net_annual / 12) - loan_payment_monthly
    return round(monthly_net, 2)

def calculate_thriving_score(net_monthly, rent, col_index, lifestyle_factor=1.0):
    """
    Returns a score 0-100.
    """
    # Estimated "Survival" Cost = Rent + Groceries/Transport
    # We estimate non-rent living costs based on COL Index
    # (COL 100 ~ $1200/mo for food/transport)
    living_cost = (col_index / 100) * 1200 * lifestyle_factor
    
    total_expenses = rent + living_cost
    discretionary_income = net_monthly - total_expenses
    
    # SCORING ALGORITHM
    # If Discretionary < $0 -> Score < 40 (Failing)
    # If Discretionary = $1000 -> Score 75 (Comfortable)
    # If Discretionary > $2000 -> Score 95+ (Thriving)
    
    score = 40 + (discretionary_income / 35)
    
    return int(max(0, min(100, score)))