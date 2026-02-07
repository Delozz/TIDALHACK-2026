import google.generativeai as genai


def get_lifestyle_reality_check(api_key, city, debt, lifestyle):
    """
    Agent 1: The Financial Realist.
    Generates a 'Vibe Check' based on the user's debt and lifestyle choice.
    """
    if not api_key:
        return "Please enter an API Key."

    # CONFIGURE
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return f"Configuration Error: {str(e)}"

    prompt = f"""
    Act as a 'Financial Big Brother' for a new college grad.
    
    User Profile:
    - Target City: {city}
    - Student Loans: ${debt}
    - Lifestyle Preference: {lifestyle} (Options: Frugal, Balanced, Boujee)
    
    Task:
    Write a 3-sentence 'Reality Check'.
    1. Can they afford this lifestyle in this city with that debt?
    2. What is the harsh reality (e.g., "You will need 3 roommates")?
    3. End with one helpful tip for that specific city.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"LIFESTYLE AGENT ERROR: {e}")
        return "⚠️ AI Error: Check your API Key or Quota."


def get_career_advice(api_key, resume_data, target_city):
    """
    Agent 2: The Career Coach.
    Suggests a specific 'Pivot' to help them succeed in the target city.
    """
    if not api_key:
        return "Please enter an API Key."

    genai.configure(api_key=api_key)
    # CHANGED: Removed 'self.' and used a valid model name
    model = genai.GenerativeModel('gemini-1.5-flash')

    # SAFEGUARD: Handle cases where no skills are found
    raw_skills = resume_data.get('skills', [])
    skills = ", ".join(
        raw_skills) if raw_skills else "General student background"
    major = resume_data.get('major', 'General')

    prompt = f"""
    User is a {major} major looking for a job in {target_city}.
    Their Current Skills: {skills}.
    
    Task:
    1. Suggest 1 specific job title that fits them in {target_city}.
    2. Suggest 1 specific project or certification they should do to increase their salary.
    
    Keep it short and actionable (bullet points).
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"CAREER AGENT ERROR: {e}")
        return "Focus on building a portfolio relevant to local industries."
