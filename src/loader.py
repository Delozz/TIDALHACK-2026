# src/loader.py
import pandas as pd
import streamlit as st

# --- CONFIGURATION ---
CAREER_BASE_SALARIES = {
    'Software Engineer': 115000,
    'Data Scientist': 110000,
    'Cybersecurity Analyst': 105000,
    'UX Designer': 95000,
    'Product Manager': 120000
}

# Tier Multipliers (Higher Tier = Higher Salary)
TIER_MULTIPLIERS = {
    1: 1.35,  # SF, NYC
    2: 1.15,  # Austin, Denver
    3: 0.95,  # Raleigh, SLC
    4: 0.85   # College Towns
}

BASE_CITIES = [
    # Tier 1
    {'City': 'San Francisco', 'State': 'CA', 'Tier': 1, 'Lat': 37.77, 'Lon': -122.41, 'Rent': 3200, 'COL': 96},
    {'City': 'New York', 'State': 'NY', 'Tier': 1, 'Lat': 40.71, 'Lon': -74.00, 'Rent': 3600, 'COL': 100},
    {'City': 'Seattle', 'State': 'WA', 'Tier': 1, 'Lat': 47.60, 'Lon': -122.33, 'Rent': 2300, 'COL': 85},
    {'City': 'Boston', 'State': 'MA', 'Tier': 1, 'Lat': 42.36, 'Lon': -71.05, 'Rent': 2700, 'COL': 88},
    
    # Tier 2
    {'City': 'Austin', 'State': 'TX', 'Tier': 2, 'Lat': 30.26, 'Lon': -97.74, 'Rent': 1700, 'COL': 65},
    {'City': 'Denver', 'State': 'CO', 'Tier': 2, 'Lat': 39.73, 'Lon': -104.99, 'Rent': 1900, 'COL': 68},
    {'City': 'Chicago', 'State': 'IL', 'Tier': 2, 'Lat': 41.87, 'Lon': -87.62, 'Rent': 2000, 'COL': 70},
    {'City': 'Atlanta', 'State': 'GA', 'Tier': 2, 'Lat': 33.74, 'Lon': -84.38, 'Rent': 1800, 'COL': 66},

    # Tier 3
    {'City': 'Raleigh', 'State': 'NC', 'Tier': 3, 'Lat': 35.77, 'Lon': -78.63, 'Rent': 1400, 'COL': 63},
    {'City': 'Huntsville', 'State': 'AL', 'Tier': 3, 'Lat': 34.73, 'Lon': -86.58, 'Rent': 1100, 'COL': 55},
    {'City': 'Columbus', 'State': 'OH', 'Tier': 3, 'Lat': 39.96, 'Lon': -82.99, 'Rent': 1200, 'COL': 58},
    
    # Tier 4
    {'City': 'College Station', 'State': 'TX', 'Tier': 4, 'Lat': 30.62, 'Lon': -96.33, 'Rent': 900, 'COL': 50},
    {'City': 'Ann Arbor', 'State': 'MI', 'Tier': 4, 'Lat': 42.28, 'Lon': -83.74, 'Rent': 1800, 'COL': 68},
]

@st.cache_data
def load_all_salaries():
    """
    Generates the Cross-Product of Cities X Careers.
    """
    data = []
    
    for city in BASE_CITIES:
        for career, base_salary in CAREER_BASE_SALARIES.items():
            
            # Calculate Localized Salary
            tier_adjust = TIER_MULTIPLIERS.get(city['Tier'], 1.0)
            projected_salary = int(base_salary * tier_adjust)
            
            data.append({
                'City': city['City'],
                'State': city['State'],
                'Lat': city['Lat'],
                'Lon': city['Lon'],
                'Rent': city['Rent'],
                'COL': city['COL'],
                'Category': career,        # Replaces 'Role'
                'Salary': projected_salary
            })
            
    return pd.DataFrame(data)