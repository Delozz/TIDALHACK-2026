import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils.loader import load_all_salaries
from src.logic import calculate_taxes, project_savings, calculate_thriving_score

# --- PAGE SETUP ---
st.set_page_config(page_title="NextStep", page_icon="🎓", layout="wide")

# --- LOAD DATA ---
df = load_all_salaries()

# --- CUSTOM STYLING FUNCTION ---
def style_metric_cards():
    """Inject CSS to style metric cards with modern SaaS look"""
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: white; }
        div.stButton > button { background-color: #FF4B4B; color: white; border-radius: 10px; }
        
        /* Metric Card Styling */
        div[data-testid="stMetricValue"] { 
            font-size: 50px; 
        }
        div[data-testid="stMetric"] {
            background-color: #1E2130;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #2E3440;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #1E2130;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FF4B4B;
        }
        </style>
        """, unsafe_allow_html=True)

# Apply custom styling
style_metric_cards()

# --- SIDEBAR: USER INPUTS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("NextStep")
    st.write("Plan your life after the cap and gown.")
    
    selected_category = st.selectbox("Select your Career Path", df['Category'].unique())
    debt = st.number_input("Student Loan Debt ($)", min_value=0, max_value=500000, value=30000, step=1000)
    lifestyle = st.select_slider("Lifestyle Preference", options=["Frugal", "Balanced", "Boujee"])
    
    st.divider()
    
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    
    if st.button("Calculate Future"):
        st.session_state['selected_category'] = selected_category
        st.success("Crunching the numbers...")

# --- FILTER DATA BASED ON SELECTION ---
filtered_data = df[df['Category'] == selected_category]

# --- MOCK DATA (Fallback for development) ---
df_mock = pd.DataFrame({
    'City': ['Austin', 'Seattle', 'New York', 'Denver'],
    'Lat': [30.26, 47.60, 40.71, 39.73],
    'Lon': [-97.74, -122.33, -74.00, -104.99],
    'Score': [88, 75, 60, 82],
    'Salary': [95000, 130000, 145000, 110000],
    'Rent': [1200, 1800, 2800, 1400],
    'Jobs': [450, 620, 890, 320]
})

# --- DYNAMIC METRICS CALCULATION ---
if not filtered_data.empty:
    # Find the city with highest salary (or Score if Salary doesn't exist)
    if 'Salary' in filtered_data.columns:
        top_city_row = filtered_data.loc[filtered_data['Salary'].idxmax()]
        top_metric_value = f"${top_city_row['Salary']:,.0f}"
        metric_col = 'Salary'
    elif 'Score' in filtered_data.columns:
        top_city_row = filtered_data.loc[filtered_data['Score'].idxmax()]
        top_metric_value = f"{top_city_row['Score']}/100"
        metric_col = 'Score'
    else:
        # Fallback if neither column exists
        top_city_row = filtered_data.iloc[0]
        top_metric_value = "N/A"
        metric_col = None
    
    top_city = top_city_row['City'] if 'City' in top_city_row else "Unknown"
    avg_salary = filtered_data['Salary'].mean() if 'Salary' in filtered_data.columns else 0
    
    # For display purposes
    data_for_display = filtered_data
else:
    # Fallback to mock data if filtered_data is empty
    top_city = "Austin"
    top_metric_value = "$95,000"
    avg_salary = 120000
    data_for_display = df_mock

# --- KEY METRICS ROW ---
col1, col2, col3 = st.columns(3)
col1.metric("Top City Match", top_city, "Highest Pay" if not filtered_data.empty else "Mock Data")
col2.metric("Projected Savings", "$1,204/mo", "-5% vs avg")
col3.metric("Average Salary", f"${avg_salary:,.0f}" if avg_salary > 0 else "N/A", "For this role")

st.divider()

# --- TABBED INTERFACE ---
tab1, tab2, tab3 = st.tabs(["Map View", "Budget Lab", "Resume Pivot"])

# ========== TAB 1: MAP VIEW ==========
with tab1:
    st.subheader(f"Where can a {selected_category} thrive?")
    
    # Check if we have data for this career path
    if filtered_data.empty:
        st.warning("⚠️ No data found for this career path yet. Showing mock data for demonstration.")
        map_data = df_mock
        spotlight_city = "Austin, Texas"
        spotlight_text = "Highest 'Thriving Score' for this career. No State Income Tax saves you **$4,200/year**."
    else:
        map_data = filtered_data
        # Get top city from filtered data
        if 'Salary' in filtered_data.columns:
            top_row = filtered_data.loc[filtered_data['Salary'].idxmax()]
            spotlight_city = top_row['City'] if 'City' in top_row else "Top City"
            spotlight_salary = f"${top_row['Salary']:,.0f}" if 'Salary' in top_row else "N/A"
            spotlight_text = f"Highest salary for {selected_category}: **{spotlight_salary}/year**"
        else:
            spotlight_city = filtered_data.iloc[0]['City'] if 'City' in filtered_data.columns else "Top City"
            spotlight_text = f"Best match for {selected_category} professionals."
    
    # Create a 'Spotlight' section for the #1 city
    with st.container():
        st.markdown("### 🌟 Your Best Move")
        inner_col1, inner_col2 = st.columns([1, 2])
        with inner_col1:
            st.image("https://img.icons8.com/fluency/96/star.png")  # Or a city icon
        with inner_col2:
            st.subheader(spotlight_city)
            st.write(spotlight_text)
    
    st.divider()
    
    # Determine which columns to use for the map
    has_lat_lon = 'Lat' in map_data.columns and 'Lon' in map_data.columns
    has_score = 'Score' in map_data.columns
    has_salary = 'Salary' in map_data.columns
    
    if has_lat_lon and (has_score or has_salary):
        # Enhanced scatter geo map (no token required)
        size_col = 'Score' if has_score else 'Salary'
        color_col = 'Score' if has_score else 'Salary'
        
        # Build hover_data dynamically
        hover_data_dict = {}
        if has_score:
            hover_data_dict['Score'] = True
        if has_salary:
            hover_data_dict['Salary'] = ':$,.0f'
        if 'Rent' in map_data.columns:
            hover_data_dict['Rent'] = ':$,.0f'
        if 'Jobs' in map_data.columns:
            hover_data_dict['Jobs'] = True
        hover_data_dict['Lat'] = False
        hover_data_dict['Lon'] = False
        
        fig_map = px.scatter_geo(
            map_data,
            lat="Lat",
            lon="Lon",
            size=size_col,
            color=color_col,
            hover_name="City",
            hover_data=hover_data_dict,
            color_continuous_scale="Viridis",
            size_max=30,
            scope="usa",
            title=f"Best Cities for {selected_category}"
        )
        
        fig_map.update_layout(
            height=600,
            geo=dict(
                bgcolor='#0E1117',
                lakecolor='#1E2130',
                landcolor='#1E2130',
                showlakes=True,
                showcountries=True,
                countrycolor='#2E3440'
            ),
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.error("Map data is missing required columns (Lat, Lon, Score/Salary). Please check your data source.")
    
    with st.expander("See the math behind your score"):
        st.write(f"Based on a {lifestyle} lifestyle with ${debt:,} in debt...")
        if not filtered_data.empty:
            st.dataframe(filtered_data.head(10))

# ========== TAB 2: BUDGET LAB ==========
with tab2:
    st.subheader("Financial Reality Check")
    
    # Add city selector for deep dive analysis
    if not filtered_data.empty and 'City' in filtered_data.columns:
        target_city = st.selectbox('🎯 Analyze a City', filtered_data['City'].unique())
        
        # Get the specific city data
        city_data = filtered_data[filtered_data['City'] == target_city].iloc[0]
        
        # Extract city-specific values
        city_salary = city_data.get('Salary', 100000)
        city_rent = city_data.get('Rent', 1500)
        city_state = city_data.get('State', 'TX')  # Default to TX if not available
        
        # Calculate real financial metrics using logic functions
        monthly_net = calculate_taxes(city_salary, city_state)
        
        # Estimate monthly loan payment (10-year standard repayment)
        monthly_loan_payment = (debt / 10000) * 115
        
        # Estimate lifestyle costs based on user's preference
        lifestyle_costs = {
            'Frugal': 900,
            'Balanced': 1700,
            'Boujee': 3000
        }
        lifestyle_cost = lifestyle_costs.get(lifestyle, 1700)
        
        # Calculate projected savings
        monthly_savings = project_savings(monthly_net, city_rent, monthly_loan_payment, lifestyle_cost)
        
        # Calculate taxes paid (for donut chart)
        gross_monthly = city_salary / 12
        taxes_paid = gross_monthly - monthly_net
        
    else:
        # Fallback to mock data
        st.warning("⚠️ No city data available. Using sample calculations.")
        target_city = "Austin"
        city_salary = 100000
        city_rent = 1200
        city_state = "TX"
        monthly_net = 5862
        monthly_loan_payment = 300
        lifestyle_cost = 1700
        monthly_savings = 2362
        taxes_paid = 1471
    
    left_col, right_col = st.columns([1, 1])
    
    # Left Column: Donut Chart
    with left_col:
        st.markdown("### Monthly Budget Breakdown")
        
        # Real budget data based on calculations
        budget_data = {
            'Category': ['Rent', 'Taxes', 'Loans', 'Lifestyle', 'Savings'],
            'Amount': [
                city_rent,
                taxes_paid,
                monthly_loan_payment,
                lifestyle_cost,
                max(0, monthly_savings)  # Show 0 if negative
            ]
        }
        df_budget = pd.DataFrame(budget_data)
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=df_budget['Category'],
            values=df_budget['Amount'],
            hole=0.5,
            marker=dict(
                colors=['#FF4B4B', '#FFA500', '#FFD700', '#9D4EDD', '#00D9FF'],
                line=dict(color='#0E1117', width=2)
            ),
            textfont=dict(size=16, color='white')
        )])
        
        fig_donut.update_layout(
            showlegend=True,
            height=400,
            paper_bgcolor='#0E1117',
            plot_bgcolor='#0E1117',
            font=dict(color='white', size=14),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
        
        # Dynamic insight sentence
        if monthly_savings > 0:
            st.success(f"💰 In **{target_city}**, you will have **${monthly_savings:,.2f}** left over for fun/investing each month.")
        else:
            st.error(f"⚠️ In **{target_city}**, you may overspend by **${abs(monthly_savings):,.2f}** per month with a {lifestyle} lifestyle.")
    
    # Right Column: Success Checklist & Updated Metrics
    with right_col:
        st.markdown("### 📊 Key Financial Metrics")
        
        # Display key metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Monthly Net Pay", f"${monthly_net:,.0f}", "After taxes")
            st.metric("Monthly Expenses", f"${(city_rent + lifestyle_cost + monthly_loan_payment):,.0f}", "Total")
        with col_b:
            st.metric("Projected Savings", f"${monthly_savings:,.0f}/mo", 
                     "💰" if monthly_savings > 1000 else ("⚠️" if monthly_savings < 0 else "📊"))
            st.metric("Annual Savings", f"${monthly_savings * 12:,.0f}/yr", "If consistent")
        
        st.divider()
        
        st.markdown("### Success Checklist")
        st.markdown("Track your financial milestones:")
        
        st.checkbox("✅ Emergency Fund Built (3-6 months)", value=False)
        st.checkbox("✅ 401k Maxed ($23,000/year)", value=False)
        st.checkbox("✅ High-Interest Debt Paid Off", value=True)
        st.checkbox("✅ Credit Score Above 750", value=True)
        st.checkbox("✅ Side Income Stream Active", value=False)
        st.checkbox("✅ Monthly Budget Tracked", value=True)
        st.checkbox("✅ Investment Portfolio Started", value=False)
        st.checkbox("✅ Health Insurance Secured", value=True)


# ========== TAB 3: RESUME PIVOT ==========
with tab3:
    st.subheader("Resume Analysis & Career Pivot")
    
    # Hardcoded dictionary of hot keywords for STEM careers
    STEM_KEYWORDS = {
        'Data Scientist': ['Python', 'SQL', 'TensorFlow', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-learn', 'Statistics', 'A/B Testing', 'PyTorch'],
        'Cybersecurity Analyst': ['Firewalls', 'Penetration Testing', 'Security', 'SIEM', 'Risk Assessment', 'Encryption', 'Network Security', 'Incident Response', 'Compliance', 'Threat Analysis'],
        'Software Engineer': ['Python', 'Java', 'JavaScript', 'React', 'Node.js', 'Git', 'API', 'AWS', 'Docker', 'Agile'],
        'Machine Learning Engineer': ['Python', 'TensorFlow', 'PyTorch', 'Deep Learning', 'Neural Networks', 'MLOps', 'Kubernetes', 'Model Deployment', 'Computer Vision', 'NLP'],
        'Cloud Architect': ['AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker', 'Terraform', 'CI/CD', 'Microservices', 'Cloud Security', 'DevOps'],
        'Data Engineer': ['Python', 'SQL', 'Spark', 'Hadoop', 'ETL', 'Data Pipeline', 'Airflow', 'Kafka', 'Snowflake', 'BigQuery'],
        'DevOps Engineer': ['Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 'Linux', 'Terraform', 'Ansible', 'Git', 'AWS', 'Monitoring']
    }
    
    # Get relevant keywords for selected career
    relevant_keywords = STEM_KEYWORDS.get(selected_category, ['Python', 'SQL', 'Git', 'Communication', 'Problem Solving'])
    
    if uploaded_file is not None:
        st.success(f"✅ Resume uploaded: **{uploaded_file.name}**")
        
        # Try to extract text from PDF
        resume_text = ""
        try:
            # Attempt to use pypdf if available
            import pypdf
            pdf_reader = pypdf.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text().upper()
        except ImportError:
            # Fallback: Mock resume text for demo if pypdf not installed
            st.info("📝 Using demo analysis mode (install pypdf for real PDF parsing)")
            resume_text = """
            EXPERIENCED SOFTWARE ENGINEER WITH PYTHON, JAVASCRIPT, AND REACT EXPERIENCE.
            WORKED WITH AWS, DOCKER, AND GIT IN PRODUCTION ENVIRONMENTS.
            STRONG BACKGROUND IN MACHINE LEARNING AND DATA ANALYSIS.
            PROFICIENT IN SQL AND DATABASE DESIGN.
            """.upper()
        except Exception as e:
            st.warning(f"Could not parse PDF: {e}. Using demo mode.")
            resume_text = "PYTHON SQL AWS DOCKER GIT".upper()
        
        st.divider()
        
        # Keyword Analysis Section
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("### 🎯 Keywords Found")
            st.caption("Skills detected in your resume")
            
            found_keywords = []
            for keyword in relevant_keywords:
                if keyword.upper() in resume_text:
                    found_keywords.append(keyword)
                    st.markdown(f"<div style='background-color: #1a4d2e; padding: 8px; margin: 4px 0; border-radius: 5px; border-left: 4px solid #00ff88;'>✅ <b>{keyword}</b> detected</div>", unsafe_allow_html=True)
            
            if not found_keywords:
                st.warning("No keywords detected. Make sure your resume includes technical skills!")
        
        with col_right:
            st.markdown("### 📈 Skills to Add")
            st.caption("Boost your resume with these")
            
            missing_keywords = []
            for keyword in relevant_keywords:
                if keyword.upper() not in resume_text:
                    missing_keywords.append(keyword)
                    st.markdown(f"<div style='background-color: #4d1a1a; padding: 8px; margin: 4px 0; border-radius: 5px; border-left: 4px solid #ff4444;'>❌ <b>{keyword}</b> - Recommended</div>", unsafe_allow_html=True)
            
            if not missing_keywords:
                st.success("🎉 You have all the key skills!")
        
        st.divider()
        
        # Analysis Summary
        st.markdown("### 📊 Analysis Summary")
        match_percentage = (len(found_keywords) / len(relevant_keywords)) * 100 if relevant_keywords else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Keywords Found", f"{len(found_keywords)}/{len(relevant_keywords)}", f"{match_percentage:.0f}% match")
        col2.metric("Skills Gap", len(missing_keywords), "to learn")
        col3.metric("Career Fit", "Strong" if match_percentage > 60 else ("Medium" if match_percentage > 30 else "Growing"), 
                   "🎯" if match_percentage > 60 else "📈")
        
        # Progress bar
        st.progress(match_percentage / 100)
        st.caption(f"Your resume matches {match_percentage:.0f}% of key skills for {selected_category} roles")
        
        # Action items
        if missing_keywords:
            with st.expander("💡 Action Plan to Close the Gap"):
                st.markdown("**Recommended next steps:**")
                for i, keyword in enumerate(missing_keywords[:5], 1):  # Show top 5
                    st.write(f"{i}. Learn **{keyword}** - Add to resume once proficient")
                st.write("\n**Resources:**")
                st.write("- Online courses: Coursera, Udemy, freeCodeCamp")
                st.write("- Practice projects: GitHub, Kaggle, personal portfolio")
                st.write("- Certifications: AWS, Google Cloud, CompTIA")
    
    else:
        # No file uploaded - show prompt
        st.warning("📄 Upload your resume in the sidebar to get an instant keyword analysis!")
        
        st.markdown("---")
        
        # Preview of what they'll get
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🔍 What We Analyze")
            st.write(f"✓ **{len(relevant_keywords)} key skills** for {selected_category}")
            st.write("✓ **ATS-friendly keywords** (what recruiters search for)")
            st.write("✓ **Skills gap analysis** to prioritize learning")
            st.write("✓ **Career fit score** for your target role")
        
        with col_b:
            st.markdown("#### 🎯 Hot Keywords for Your Role")
            st.caption(f"Top skills for {selected_category}:")
            for keyword in relevant_keywords[:6]:  # Show first 6
                st.markdown(f"<div style='background-color: #1E2130; padding: 6px 12px; margin: 4px 0; border-radius: 5px; display: inline-block;'>🔹 {keyword}</div>", unsafe_allow_html=True)