# src/logic.py

def calculate_net_monthly(gross_salary, debt_amount):
    """
    Estimates monthly take-home pay.
    """
    monthly_gross = gross_salary / 12
    
    # 1. TAXES
    # Federal + FICA is ~22%. 
    # We add a flat 5% buffer for State/Local tax variances.
    effective_tax_rate = 0.27 
    taxes = monthly_gross * effective_tax_rate
    
    # 2. LOANS
    # Standard Repayment: ~$120/mo per $10k debt
    loan_payment = (debt_amount / 10000) * 120
    
    net = monthly_gross - taxes - loan_payment
    return net

def get_thriving_score(net_monthly, rent_cost, col_index):
    """
    Calculates the 'Thriving Score' (0-100).
    Now with Rent Burden Penalty!
    """
    # 1. ESTIMATE LIVING COSTS (Non-Rent)
    # Baseline: Index 100 (NYC) = ~$1,800/mo for food/transport/fun
    est_living_expenses = (col_index / 100) * 1800
    
    # 2. TOTAL MONTHLY SPEND
    total_cost = rent_cost + est_living_expenses
    
    # 3. DISCRETIONARY INCOME (Money left over)
    discretionary = net_monthly - total_cost
    
    # --- SCORING ALGORITHM (STRICTER) ---
    
    # Base Score starts at 50 (Survival)
    score = 50
    
    # Bonus: +1 point for every $60 of extra cash (Harder to earn points)
    score += (discretionary / 60)
    
    # PENALTY: Rent Burden
    # Financial Advice: Rent should not exceed 30% of Net Income.
    rent_ratio = rent_cost / net_monthly
    if rent_ratio > 0.30:
        # If rent is 40% of income, penalize (40 - 30) * 2 = 20 points
        penalty = (rent_ratio - 0.30) * 100 * 2
        score -= penalty
        
    # Cap it between 0 and 100
    return int(max(0, min(100, score)))