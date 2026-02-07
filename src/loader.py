# src/loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_all_salaries():
    """
    Reads multiple CSVs, standardizes column names, and merges them into one Master DataFrame.
    """
    all_data_frames = []

    # --- FILE CONFIGURATION ---
    # Map the filename to the Category Name you want in the UI
    files_to_load = {
        'data/raw_salaries/ds_salaries.csv': 'Data Science',
        'data/raw_salaries/salaries_cyber.csv': 'Cybersecurity',
        'data/raw_salaries/aisalaries.csv': 'AI/ML'
    }

    for file_path, category_name in files_to_load.items():
        try:
            # 1. Read the file
            df = pd.read_csv(file_path)
            
            # 2. Add the Category Tag
            df['Category'] = category_name
            
            # 3. STANDARDIZE COLUMNS (Crucial Step!)
            # Different CSVs have different names. We map them to our Standard Names.
            # You might need to adjust the keys (left side) based on your specific CSVs.
            
            # Example: If DS file has 'salary_in_usd' but Cyber file has 'base_pay'
            if 'salary_in_usd' in df.columns:
                df = df.rename(columns={'salary_in_usd': 'Salary', 'company_location': 'Location'})
            elif 'base_pay' in df.columns:
                df = df.rename(columns={'base_pay': 'Salary', 'work_location': 'Location'})
            elif 'total_compensation' in df.columns:
                df = df.rename(columns={'total_compensation': 'Salary', 'location': 'Location'})

            # 4. Keep only the columns we need to save memory
            # Ensure these columns exist now (after renaming)
            cols_to_keep = ['Category', 'Salary', 'Location'] 
            
            # (Optional: Add 'job_title' if you want it)
            if 'job_title' in df.columns: 
                cols_to_keep.append('job_title')
            elif 'Job Title' in df.columns:
                df = df.rename(columns={'Job Title': 'job_title'})
                cols_to_keep.append('job_title')

            # Filter and append
            df_clean = df[cols_to_keep].copy()
            all_data_frames.append(df_clean)
            
        except Exception as e:
            st.warning(f"Skipped {file_path}: {e}")

    # 5. Merge everything into one giant table
    if all_data_frames:
        master_df = pd.concat(all_data_frames, ignore_index=True)
        return master_df
    else:
        return pd.DataFrame() # Return empty if everything failed