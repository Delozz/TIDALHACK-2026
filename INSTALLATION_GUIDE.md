# Installation & Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages:
- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning utilities
- `plotly` - Interactive visualizations
- `joblib` - Model persistence
- `PyPDF2` - PDF parsing (legacy)
- `pypdf` - PDF parsing (modern)
- `google-generativeai` - Google Gemini AI API
- `python-dotenv` - Environment variable management

### 2. Set Up API Key

Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_api_key_here
```

See `API_SETUP.md` for detailed instructions on obtaining a Gemini API key.

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501` (or another port if 8501 is in use).

## Troubleshooting

### "No module named 'PyPDF2'" Error
**Solution:** Install the PDF parsing packages:
```bash
pip install PyPDF2 pypdf
```

### "No module named 'google.generativeai'" Error
**Solution:** Install the Google Gemini API package:
```bash
pip install google-generativeai
```

### "GEMINI_API_KEY not found" Warning
**Solution:** 
1. Create a `.env` file in the project root
2. Add your API key: `GEMINI_API_KEY=your_key_here`
3. Restart the Streamlit app

### Resume Upload Not Working
**Symptoms:** "AI Analysis failed: No module named 'PyPDF2'"

**Solution:**
1. Install required packages: `pip install PyPDF2 pypdf`
2. Restart Streamlit
3. Try uploading resume again

### App Stuck on "Crunching numbers..."
**Possible Causes:**
1. Missing PyPDF2 package ✅ **FIXED**
2. Invalid API key - Check your `.env` file
3. Invalid Gemini model name ✅ **FIXED** (using `gemini-1.5-flash`)

**Solution:**
- Check browser console (F12) for errors
- Check terminal output where Streamlit is running
- Verify API key is set correctly in `.env`

## Project Structure

```
TIDALHACK-2026/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not in git)
├── env.template             # Template for .env file
├── API_SETUP.md             # API key setup instructions
├── src/
│   ├── loader.py            # Data loading and generation
│   ├── logic.py             # Financial calculations
│   ├── config.py            # Configuration management
│   └── utils/
│       ├── resume_parser.py # AI-powered resume parsing
│       └── job_matcher.py   # AI career advice
└── README.md
```

## Development Tips

### Hot Reload
Streamlit automatically reloads when you save changes to `.py` files.

### Debug Mode
To see more detailed error messages, check the terminal where Streamlit is running.

### Testing Resume Analysis
1. Make sure your `.env` file has a valid `GEMINI_API_KEY`
2. Upload a PDF resume through the sidebar
3. Click "Calculate Future"
4. Watch the terminal output for any errors

### Common Streamlit Commands
- `streamlit run app.py` - Start the app
- `Ctrl+C` in terminal - Stop the app
- `streamlit cache clear` - Clear cached data

## Next Steps

After successful installation:
1. ✅ Upload a resume to test AI analysis
2. ✅ Try different career paths from the dropdown
3. ✅ Explore different cities in the Map View
4. ✅ Use the Budget Lab to analyze specific cities
5. ✅ Check the Resume Pivot tab for AI insights

## Support

If you encounter issues not covered here:
1. Check `SECURITY_UPDATE_SUMMARY.md` for recent changes
2. Check `RESULTS_DISPLAY_UPDATE.md` for UI features
3. Review error messages in the terminal
4. Verify all packages are installed: `pip list`

---

Last Updated: February 7, 2026
