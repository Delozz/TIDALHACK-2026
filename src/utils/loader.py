import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_all_salaries():
    """
    Load salary data from data/salaries.csv with caching.
    
    Returns:
        pd.DataFrame: DataFrame with salary data including columns 
                      ['Category', 'City', 'Salary']
    
    If the file is missing, returns a mock DataFrame with dummy STEM data
    to prevent the app from crashing during development.
    """
    file_path = "data/salaries.csv"
    
    try:
        # Attempt to load the CSV file
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            # File doesn't exist, return mock data
            return _create_mock_salary_data()
    
    except Exception as e:
        # If any error occurs during loading, fall back to mock data
        st.warning(f"Could not load {file_path}: {e}. Using mock data instead.")
        return _create_mock_salary_data()


def _create_mock_salary_data():
    """
    Create mock STEM salary data for development/fallback purposes.
    
    Returns:
        pd.DataFrame: Mock DataFrame with STEM job categories, cities, and salaries
    """
    mock_data = {
        'Category': [
            'Data Scientist',
            'Cybersecurity Analyst',
            'Software Engineer',
            'Machine Learning Engineer',
            'Cloud Architect'
        ],
        'City': [
            'San Francisco',
            'Austin',
            'Seattle',
            'Boston',
            'Denver'
        ],
        'Salary': [
            145000,
            95000,
            130000,
            155000,
            125000
        ]
    }
    
    return pd.DataFrame(mock_data)
