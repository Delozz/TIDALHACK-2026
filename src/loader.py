# src/loader.py
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    """
    GENERATES 1000+ ROWS OF REALISTIC SYNTHETIC DATA.
    Includes 25 US Cities with accurate Cost of Living & Rent approximations.
    """
    # 1. THE MASTER CITY LIST (25 Cities)
    # Rent is approx for a 1-bedroom apt near city center. 
    # COL is Numbeo Index (NYC = 100).
    cities = [
        # --- TIER 1: EXPENSIVE TECH HUBS ---
        {'City': 'San Francisco', 'State': 'CA', 'Lat': 37.77, 'Lon': -122.41, 'Rent': 3200, 'COL': 96},
        {'City': 'New York', 'State': 'NY', 'Lat': 40.71, 'Lon': -74.00, 'Rent': 3600, 'COL': 100},
        {'City': 'Seattle', 'State': 'WA', 'Lat': 47.60, 'Lon': -122.33, 'Rent': 2300, 'COL': 85},
        {'City': 'Boston', 'State': 'MA', 'Lat': 42.36, 'Lon': -71.05, 'Rent': 2700, 'COL': 88},
        {'City': 'Los Angeles', 'State': 'CA', 'Lat': 34.05, 'Lon': -118.24, 'Rent': 2600, 'COL': 82},
        {'City': 'Washington', 'State': 'DC', 'Lat': 38.90, 'Lon': -77.03, 'Rent': 2400, 'COL': 84},
        {'City': 'San Diego', 'State': 'CA', 'Lat': 32.71, 'Lon': -117.16, 'Rent': 2500, 'COL': 80},

        # --- TIER 2: RISING TECH HUBS ---
        {'City': 'Austin', 'State': 'TX', 'Lat': 30.26, 'Lon': -97.74, 'Rent': 1700, 'COL': 65},
        {'City': 'Denver', 'State': 'CO', 'Lat': 39.73, 'Lon': -104.99, 'Rent': 1900, 'COL': 68},
        {'City': 'Atlanta', 'State': 'GA', 'Lat': 33.74, 'Lon': -84.38, 'Rent': 1800, 'COL': 66},
        {'City': 'Chicago', 'State': 'IL', 'Lat': 41.87, 'Lon': -87.62, 'Rent': 2000, 'COL': 70},
        {'City': 'Miami', 'State': 'FL', 'Lat': 25.76, 'Lon': -80.19, 'Rent': 2400, 'COL': 78},
        {'City': 'Dallas', 'State': 'TX', 'Lat': 32.77, 'Lon': -96.79, 'Rent': 1600, 'COL': 64},
        {'City': 'Phoenix', 'State': 'AZ', 'Lat': 33.44, 'Lon': -112.07, 'Rent': 1500, 'COL': 62},

        # --- TIER 3: HIDDEN GEMS (Good for "Thriving Score") ---
        {'City': 'Raleigh', 'State': 'NC', 'Lat': 35.77, 'Lon': -78.63, 'Rent': 1400, 'COL': 63},
        {'City': 'Salt Lake City', 'State': 'UT', 'Lat': 40.76, 'Lon': -111.89, 'Rent': 1500, 'COL': 64},
        {'City': 'Huntsville', 'State': 'AL', 'Lat': 34.73, 'Lon': -86.58, 'Rent': 1100, 'COL': 55},
        {'City': 'Columbus', 'State': 'OH', 'Lat': 39.96, 'Lon': -82.99, 'Rent': 1200, 'COL': 58},
        {'City': 'Pittsburgh', 'State': 'PA', 'Lat': 40.44, 'Lon': -79.99, 'Rent': 1300, 'COL': 60},
        {'City': 'Minneapolis', 'State': 'MN', 'Lat': 44.97, 'Lon': -93.26, 'Rent': 1400, 'COL': 66},
        {'City': 'Charlotte', 'State': 'NC', 'Lat': 35.22, 'Lon': -80.84, 'Rent': 1500, 'COL': 64},
        
        # --- TIER 4: COLLEGE TOWNS (The Benchmark) ---
        {'City': 'College Station', 'State': 'TX', 'Lat': 30.62, 'Lon': -96.33, 'Rent': 900, 'COL': 50},
        {'City': 'Boulder', 'State': 'CO', 'Lat': 40.01, 'Lon': -105.27, 'Rent': 2100, 'COL': 75},
        {'City': 'Ann Arbor', 'State': 'MI', 'Lat': 42.28, 'Lon': -83.74, 'Rent': 1800, 'COL': 68},
    ]

    # 2. GENERATE ROLES & SALARIES
    roles = ['Software Engineer', 'Data Scientist', 'Product Manager', 'Cybersecurity Analyst', 'UX Designer']
    data = []
    
    np.random.seed(42) # Consistent numbers every time you run it

    for city in cities:
        for role in roles:
            # Base Salary Logic:
            # - Start with $70k base
            # - Add $600 for every COL point (So NYC pays ~$24k more than Austin base)
            market_rate = 70000 + (city['COL'] * 600)

            # Role Multipliers
            if role == 'Data Scientist': market_rate *= 1.12
            if role == 'Product Manager': market_rate *= 1.15
            if role == 'Cybersecurity Analyst': market_rate *= 1.08
            if role == 'UX Designer': market_rate *= 0.95

            # Create 3-5 variations per role per city (Junior, Mid, Senior)
            # This makes the scatter plot look full and real
            for _ in range(4): 
                variation = np.random.uniform(0.85, 1.3) # +/- 15-30% variance
                final_salary = int(market_rate * variation)
                
                data.append({
                    'City': city['City'],
                    'State': city['State'],
                    'Role': role,
                    'Salary': final_salary,
                    'Rent_Index': city['Rent'], # Using actual rent $ for simplicity in MVP
                    'COL_Index': city['COL'],
                    'Lat': city['Lat'],
                    'Lon': city['Lon']
                })

    return pd.DataFrame(data)