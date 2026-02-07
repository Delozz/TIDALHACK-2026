import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(page_title="NextStep", page_icon="🎓", layout="wide")

# --- CUSTOM CSS (To make it look like Tempo/Modern) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    div.stButton > button { background-color: #FF4B4B; color: white; border-radius: 10px; }
    div[data-testid="stMetricValue"] { font-size: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: USER INPUTS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("NextStep")
    st.write("Plan your life after the cap and gown.")
    
    major = st.selectbox("Select your Major", ["Computer Science", "Biology", "Finance", "Arts"])
    debt = st.slider("Student Loan Debt ($)", 0, 200000, 30000)
    lifestyle = st.select_slider("Lifestyle Preference", options=["Frugal", "Balanced", "Boujee"])
    
    st.divider() # Visual separator
    
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    
    if st.button("Calculate Future"):
        st.success("Crunching the numbers...")

# --- MAIN PAGE: THE DASHBOARD ---
# Row 1: Key Metrics (The "Wow" Factor)
col1, col2, col3 = st.columns(3)
col1.metric("Top City Match", "Austin, TX", "High Growth")
col2.metric("Projected Savings", "$1,204/mo", "-5% vs avg")
col3.metric("Thriving Score", "88/100", "Excellent")

# Row 2: The Map
st.subheader(f"Where can a {major} major thrive?")

# (Mock Data for Person B to visualize - Person A will replace this later)
df_mock = pd.DataFrame({
    'City': ['Austin', 'Seattle', 'New York', 'Denver'],
    'Lat': [30.26, 47.60, 40.71, 39.73],
    'Lon': [-97.74, -122.33, -74.00, -104.99],
    'Score': [88, 75, 60, 82]
})

# Interactive Map using Plotly
fig = px.scatter_mapbox(df_mock, lat="Lat", lon="Lon", size="Score", color="Score",
                        hover_name="City", size_max=15, zoom=3, mapbox_style="carto-darkmatter")
st.plotly_chart(fig, use_container_width=True)

# Row 3: Deep Dive Data
with st.expander("See the math behind your score"):
    st.write(f"Based on a {lifestyle} lifestyle with ${debt} in debt...")
    st.dataframe(df_mock) # Shows the raw data table