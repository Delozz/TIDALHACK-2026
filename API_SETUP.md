# Environment Setup Instructions

## Setting Up API Keys

This project uses Google Gemini AI for resume parsing and career advice features.

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Create `.env` File

Create a file named `.env` in the root directory of the project:

```bash
# In the project root directory
touch .env
```

### Step 3: Add Your API Key

Open the `.env` file and add your API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Example:**
```
GEMINI_API_KEY=AIzaSyAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPp
```

### Step 4: Install Required Dependencies

Make sure you have `python-dotenv` installed:

```bash
pip install python-dotenv google-generativeai PyPDF2
```

## Security Notes

⚠️ **IMPORTANT:**
- Never commit your `.env` file to git
- The `.env` file is already listed in `.gitignore`
- Never share your API key publicly
- If you accidentally expose your API key, delete it immediately from Google AI Studio and generate a new one

## Testing Your Setup

To verify your API key is working:

```python
from src.utils.resume_parser import AIResumeParser

# This should work without errors if your .env is set up correctly
parser = AIResumeParser()
print("✅ API key loaded successfully!")
```

## Alternative: Pass API Key Directly (Not Recommended for Production)

If you prefer not to use environment variables (for testing only):

```python
from src.utils.resume_parser import AIResumeParser

parser = AIResumeParser(api_key="your_key_here")
```

**Note:** This method is NOT recommended for production or when committing code.
