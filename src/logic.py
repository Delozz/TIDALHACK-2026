# src/logic.py

def format_currency(amount):
    return f"${int(amount):,}"

def calculate_taxes(gross_salary, state):
    # Same as before...
    fed_tax = 0.22
    no_tax_states = ['TX', 'FL', 'WA', 'NV', 'TN', 'NH', 'SD', 'WY', 'AK']
    state_tax = 0.00 if state in no_tax_states else 0.05
    monthly_net = (gross_salary * (1 - (fed_tax + state_tax))) / 12
    return int(monthly_net)

def calculate_thriving_score(monthly_net, rent, col_index):
    """
    UPDATED LOGIC: REAL PURCHASING POWER
    """
    # 1. The Rent Trap Check
    # If rent is > 30% of income, huge penalty.
    rent_ratio = rent / monthly_net
    penalty = 0
    if rent_ratio > 0.30:
        penalty = (rent_ratio - 0.30) * 150  # Steep penalty!
    
    # 2. Raw Discretionary Income
    raw_savings = monthly_net - rent
    
    # 3. PURCHASING POWER ADJUSTMENT (The Fix)
    # $1000 in NYC (Index 100) is worth $1000.
    # $1000 in Austin (Index 65) is worth $1,538.
    real_value_of_savings = raw_savings / (col_index / 100)
    
    # 4. Score Calculation
    # Baseline: $2000 "Real Value" = Score 80
    score = 40 + (real_value_of_savings / 50) - penalty
    
    return int(max(0, min(100, score)))

def project_5yr_wealth(monthly_net, rent, col_index):
    """
    Calculates 5-Year Cumulative Wealth.
    Assumes: 
    - Salary grows 5% per year
    - Rent grows 3% per year
    """
    cumulative_wealth = 0
    current_net = monthly_net
    current_rent = rent
    living_expenses = (col_index / 100) * 1200 # Baseline food/fun
    
    wealth_timeline = []
    
    for year in range(1, 6):
        yearly_savings = (current_net - current_rent - living_expenses) * 12
        cumulative_wealth += yearly_savings
        wealth_timeline.append(cumulative_wealth)
        
        # Growth for next year
        current_net *= 1.05  # 5% Raise
        current_rent *= 1.03 # 3% Rent Hike
        living_expenses *= 1.03 # Inflation
        
    return wealth_timeline[-1] # Return total after 5 years